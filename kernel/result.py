from dataclasses import dataclass
from typing import List


@dataclass
class Result:
    ok: bool
    output: dict
