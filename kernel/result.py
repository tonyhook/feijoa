from dataclasses import dataclass


@dataclass
class Result:
    ok: bool
    output: dict
