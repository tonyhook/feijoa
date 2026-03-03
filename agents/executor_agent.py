from typing import TYPE_CHECKING, cast

from kernel.agent import Agent
from kernel.event import ClarificationEvent, EventType, PlanEvent
from kernel.phase import Phase
from kernel.plan import Plan, State
from kernel.tool import Tool

if TYPE_CHECKING:
    from kernel.kernel import Kernel

class ExecutorAgent(Agent):
    allowed_phases = {Phase.SIMULATION, Phase.EXECUTION}

    def step(self, kernel: Kernel):
        mode = kernel.phase

        for planHolder in kernel.plans.values():
            plan = cast(Plan, planHolder.payload)
            if mode == Phase.SIMULATION and planHolder.state != State.SELECTED:
                continue
            if mode == Phase.EXECUTION and planHolder.state != State.SIMULATED:
                continue

            results = []
            success = True
            for step in plan.steps:
                tool = cast(Tool, kernel.tools[step.tool])

                if mode == Phase.SIMULATION:
                    r = tool.dry_run(**step.input)
                else:
                    r = tool.run(**step.input)

                results.append(r)

                if not r.ok:
                    success = False

            if mode == Phase.SIMULATION:
                planHolder.simulation_result = results
                planHolder.transition_to(State.SIMULATED)
            else:
                # Check if any result needs clarification before committing
                result_needing_clarification = next((r for r in results if r.clarification), None)
                if result_needing_clarification:
                    planHolder.transition_to(State.FAILED)
                    kernel.emit(ClarificationEvent(
                        sender = self.name,
                        type = EventType.CLARIFICATION_NEEDED,
                        payload = result_needing_clarification.clarification
                    ))
                    return

                planHolder.execution_result = results
                if success:
                    planHolder.transition_to(State.EXECUTED)
                else:
                    planHolder.transition_to(State.FAILED)

                kernel.emit(PlanEvent(
                    sender = self.name,
                    type = EventType.EXECUTION_RESULT,
                    payload = planHolder
                ))
