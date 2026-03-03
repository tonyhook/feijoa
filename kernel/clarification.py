from dataclasses import dataclass
from typing import Any, List


@dataclass
class ClarificationOption:
    label: str
    data: Any

@dataclass
class Clarification:
    question: str
    options: List[ClarificationOption]
