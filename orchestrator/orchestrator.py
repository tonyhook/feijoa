from abc import ABC, abstractmethod


class Orchestrator(ABC):

    @abstractmethod
    def handle(self, kernel):
        """
        Handle the kernel events and update the kernel phase accordingly.
        """
        pass
