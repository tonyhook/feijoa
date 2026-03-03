from dataclasses import dataclass

from kernel.clarification import Clarification


@dataclass
class Result:
    ok: bool
    output: dict
    clarification: Clarification | None = None
