import uuid

from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from kernel.result import Result


class State(Enum):
    PENDING = auto()
    SELECTED = auto()
    SIMULATED = auto()
    EXECUTED = auto()
    REJECTED = auto()
    FAILED = auto()

ALLOWED_TRANSITIONS = {
    State.PENDING: {
        State.SELECTED,
        State.REJECTED,
        State.FAILED,
    },
    State.SELECTED: {
        State.SIMULATED,
        State.FAILED,
    },
    State.SIMULATED: {
        State.EXECUTED,
        State.FAILED,
    },
    State.EXECUTED: set(),
    State.REJECTED: set(),
    State.FAILED: set(),
}

@dataclass
class Step:
    tool: str   # tool name
    input: dict # tool input parameters

@dataclass
class Plan:
    planner: str      # agent name
    steps: List[Step] # plan steps, each step corresponds to one tool call

@dataclass
class NotApplicable:
    planner: str              # agent name
    reason: str | None = None # optional reason for why the plan is not applicableß

@dataclass
class PlanHolder:
    payload: Plan | NotApplicable
    simulation_result: List[Result]
    execution_result: List[Result]
    id = uuid.uuid4().hex
    state: State = State.PENDING

    def transition_to(self, new_state: State):
        allowed = ALLOWED_TRANSITIONS[self.state]
        if new_state not in allowed:
            raise AssertionError(
                f"Illegal plan state transition: "
                f"{self.state.name} -> {new_state.name}"
            )
        self.state = new_state
