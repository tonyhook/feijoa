from abc import ABC, abstractmethod

from kernel.result import Result


class Tool(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def dry_run(self, **kwargs) -> Result:
        ...

    @abstractmethod
    def run(self, **kwargs) -> Result:
        ...
