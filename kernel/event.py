from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from kernel.plan import PlanHolder


class EventType(Enum):
    PLAN_PROPOSED = auto()
    PLAN_NOT_APPLICABLE = auto()
    PLAN_SELECTED = auto()
    SIMULATION_RESULT = auto()
    EXECUTION_RESULT = auto()


@dataclass
class Event:
    sender: str
    type: EventType
    payload: Any

@dataclass
class PlanEvent(Event):
    payload: PlanHolder
