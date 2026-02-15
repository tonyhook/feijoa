from abc import ABC, abstractmethod


class Agent(ABC):
    """
    The set of kernel phases in which this agent is allowed to step.
    Each agent category has a common set of allowed phases, it's defined in the base category class
    Individual agents cannot override those phases.
    """
    allowed_phases = set()

    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def step(self, kernel):
        """
        Execute one deterministic step.
        """
        pass
