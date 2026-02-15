import logging
from typing import List

from kernel.event import Event
from kernel.phase import Phase
from orchestrator.orchestrator import Orchestrator


logger = logging.getLogger(__name__)

class Kernel:
    phase: Phase
    events: List[Event]

    def __init__(self):
        self.phase = Phase.PLANNING
        self.events = []

    def emit(self, event: Event):
        self.events.append(event)

    def set_phase(self, phase: Phase):
        logger.info(f"Transitioning from {self.phase} to {phase}")
        self.phase = phase

    def run(self, orchestrator: Orchestrator, max_steps: int = 100):
        """
        event loop
        """
        steps = 0
        while self.phase != Phase.FINISHED and steps < max_steps:
            orchestrator.handle(self)
            steps += 1
            logger.info(f"Step {steps} completed. Current phase: {self.phase}")
