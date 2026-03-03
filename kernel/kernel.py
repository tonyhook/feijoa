import logging
from typing import Dict, List, cast

from agents.planner_agent import PlannerAgent
from kernel.agent import Agent
from kernel.clarification import Clarification, ClarificationOption
from kernel.event import Event, EventType, PlanEvent
from kernel.phase import Phase
from kernel.plan import NotApplicable, Plan, PlanHolder
from kernel.tool import Tool
from memory.memory import Memory
from orchestrator.orchestrator import Orchestrator
from tracing.trace import Trace


logger = logging.getLogger(__name__)

class Kernel:
    phase: Phase
    events: List[Event]
    agents: Dict[str, Agent]
    planners: List[PlannerAgent]
    tools: Dict[str, Tool]
    plans: Dict[str, PlanHolder]
    not_applicable_plans: Dict[str, PlanHolder]
    memory: Memory | None
    trace: Trace | None
    clarification_resolved: ClarificationOption | None
    pending_clarification: Clarification | None

    ## one single round conversation
    input: str
    output: str

    def __init__(self, memory: Memory | None = None, trace: Trace | None = None):
        self.phase = Phase.PLANNING
        self.events = []
        self.agents = {}
        self.planners = []
        self.tools = {}
        self.plans = {}
        self.not_applicable_plans = {}
        self.memory = memory
        self.trace = trace
        self.clarification_resolved = None
        self.pending_clarification = None
        self.input = ""
        self.output = ""

    def emit(self, event: Event):
        if self.trace:
            self.trace.record("EVENT_EMITTED", {"sender": event.sender, "type": event.type.name, "payload": str(event.payload)})
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
        if self.trace:
            self.trace.record("PHASE_TRANSITION", {"from": self.phase.name, "to": phase.name})
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

    def _reset_round(self):
        """Clear per-round state so PLANNING can restart cleanly."""
        self.events = []
        self.plans = {}
        self.not_applicable_plans = {}
        self.phase = Phase.PLANNING

    def run(self, orchestrator: Orchestrator, max_steps: int = 10):
        self.clarification_resolved = None
        self.input = input(">>> ")
        if self.memory:
            self.memory.add_message("user", self.input)

        steps = 0
        while self.phase != Phase.FINISHED and steps < max_steps:

            if self.phase == Phase.CLARIFICATION:
                clarification = self.pending_clarification
                if clarification:
                    print(clarification.question)
                    for i, opt in enumerate(clarification.options, 1):
                        print(f"  {i}. {opt.label}")
                    choice = input(">>> ").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(clarification.options):
                        self.clarification_resolved = clarification.options[int(choice) - 1]
                    else:
                        self.input = choice
                        self.clarification_resolved = None
                    self.pending_clarification = None
                    self._reset_round()
                continue  # re-enter loop in PLANNING phase

            for agent in self.agents.values():
                if self.phase in agent.allowed_phases:
                    logger.info(f"AGENT_STEP: {{'agent': '{agent.name}', 'phase': '{self.phase.name}'}}")
                    agent.step(self)

            orchestrator.handle(self)
            steps += 1
            logger.info(f"Step {steps} completed. Current phase: {self.phase}")

        print(self.output)
        if self.memory and self.output:
            self.memory.add_message("assistant", self.output)
