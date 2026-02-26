from abc import ABC, abstractmethod
from typing import Any, Dict


class Trace(ABC):
    
    @abstractmethod
    def record(self, event_type: str, details: Dict[str, Any]):
        pass
