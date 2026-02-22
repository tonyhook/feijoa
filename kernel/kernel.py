from typing import Dict, List, cast
import argparse
import logging

from agents.planner_agent import PlannerAgent
from kernel.agent import Agent
from kernel.event import Event, EventType, PlanEvent
from kernel.phase import Phase
from kernel.plan import NotApplicable, Plan, PlanHolder
from kernel.tool import Tool
from orchestrator.orchestrator import Orchestrator


parser = argparse.ArgumentParser(description = "Set the logging level via command line")
parser.add_argument(
    '--log',
    default = 'WARNING',
    help = 'Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)'
)
args = parser.parse_args()
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f'Invalid log level: {args.log}')
logging.basicConfig(level = numeric_level)
logger = logging.getLogger(__name__)

class Kernel:
    phase: Phase
    events: List[Event]
    agents: Dict[str, Agent]
    planners: List[PlannerAgent]
    tools: Dict[str, Tool]
    plans: Dict[str, PlanHolder]
    not_applicable_plans: Dict[str, PlanHolder]

    ## one single round conversation
    input: str
    output: str

    def __init__(self):
        self.phase = Phase.PLANNING
        self.events = []
        self.agents = {}
        self.planners = []
        self.tools = {}
        self.plans = {}
        self.not_applicable_plans = {}
        self.input = ""
        self.output = ""

    def emit(self, event: Event):
        self.events.append(event)

        if event.type == EventType.PLAN_PROPOSED:
            planEvent = cast(PlanEvent, event)
            plan = cast(Plan, planEvent.payload)
            plan_id = plan.planner
            self.plans[plan_id] = PlanHolder(
                payload = planEvent.payload,
                simulation_result = [],
                execution_result = []
            )
        if event.type == EventType.PLAN_NOT_APPLICABLE:
            planEvent = cast(PlanEvent, event)
            plan = cast(NotApplicable, planEvent.payload)
            plan_id = plan.planner
            self.not_applicable_plans[plan_id] = PlanHolder(
                payload = planEvent.payload,
                simulation_result = [],
                execution_result = []
            )

    def set_phase(self, phase):
        logger.info(f"Transitioning from {self.phase} to {phase}")
        self.phase = phase

    def register_agent(self, agent: Agent):
        if agent.name in self.agents:
            raise ValueError(f"Agent {agent.name} already registered")
        self.agents[agent.name] = agent
        if isinstance(agent, PlannerAgent):
            self.planners.append(agent)

    def register_tool(self, tool: Tool):
        if tool.name in self.tools:
            raise ValueError(f"Tool {tool.name} already registered")
        self.tools[tool.name] = tool

    def run(self, orchestrator: Orchestrator, max_steps: int = 5):
        self.input = input(">>> ")

        """
        event loop
        """
        steps = 0
        while self.phase != Phase.FINISHED and steps < max_steps:
            for agent in self.agents.values():
                if self.phase in agent.allowed_phases:
                    logger.info(f"AGENT_STEP: {{'agent': '{agent.name}', 'phase': '{self.phase.name}'}}")
                    agent.step(self)

            orchestrator.handle(self)
            steps += 1
            logger.info(f"Step {steps} completed. Current phase: {self.phase}")

        print(self.output)
