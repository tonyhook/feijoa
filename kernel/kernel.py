from typing import List
import argparse
import logging

from kernel.event import Event
from kernel.phase import Phase
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
