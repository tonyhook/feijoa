from abc import abstractmethod
from typing import TYPE_CHECKING

from kernel.agent import Agent
from kernel.event import EventType, PlanEvent
from kernel.phase import Phase
from kernel.plan import NotApplicable, Plan

if TYPE_CHECKING:
    from kernel.kernel import Kernel


class PlannerAgent(Agent):
    allowed_phases = {Phase.PLANNING}

    @abstractmethod
    def plan(self, kernel: Kernel) -> Plan | NotApplicable:
        return NotApplicable(
            planner = self.name,
            reason = "Default implementation, no plan available"
        )

    def step(self, kernel: Kernel):
        plan = self.plan(kernel)

        if plan is None or not isinstance(plan, (Plan, NotApplicable)):
            kernel.emit(PlanEvent(
                sender = self.name,
                type = EventType.PLAN_NOT_APPLICABLE,
                payload = NotApplicable(
                    reason = "Planner malfunctioning, no plan available"
                )
            ))

        if isinstance(plan, NotApplicable):
            kernel.emit(PlanEvent(
                sender = self.name,
                type = EventType.PLAN_NOT_APPLICABLE,
                payload = plan
            ))
        else:
            kernel.emit(PlanEvent(
                sender = self.name,
                type = EventType.PLAN_PROPOSED,
                payload = plan
            ))
