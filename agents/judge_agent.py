from typing import TYPE_CHECKING

from kernel.agent import Agent
from kernel.event import EventType, PlanEvent
from kernel.phase import Phase
from kernel.plan import State

if TYPE_CHECKING:
    from kernel.kernel import Kernel

class JudgeAgent(Agent):
    allowed_phases = {Phase.DECISION, Phase.SIMULATION}

    def step(self, kernel: Kernel):
        if kernel.phase == Phase.DECISION:
            candidates = [p for p in kernel.plans.values() if p.state == State.PENDING]

            if not candidates:
                return

            """
            TODO: Implement more sophisticated judging criteria
            """
            winner = candidates[0]

            for plan in candidates:
                if plan != winner:
                    plan.transition_to(State.REJECTED)

            winner.transition_to(State.SELECTED)

            kernel.emit(PlanEvent(
                sender = self.name,
                type = EventType.PLAN_SELECTED,
                payload = winner
            ))

        elif kernel.phase == Phase.SIMULATION:
            candidates = [p for p in kernel.plans.values() if p.state == State.SIMULATED]

            if not candidates:
                return

            winner = candidates[0]

            kernel.emit(PlanEvent(
                sender = self.name,
                type = EventType.SIMULATION_RESULT,
                payload = winner
            ))
