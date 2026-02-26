from abc import ABC, abstractmethod
from typing import Dict, List


class Memory(ABC):

    @abstractmethod
    def add_message(self, role: str, content: str):
        pass

    @abstractmethod
    def get_context(self) -> List[Dict[str, str]]:
        pass
