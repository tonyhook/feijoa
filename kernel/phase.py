from enum import Enum, auto


class Phase(Enum):
    PLANNING = auto()
    DECISION = auto()
    SIMULATION = auto()
    EXECUTION = auto()
    CLARIFICATION = auto()
    FINISHED = auto()
