from dataclasses import dataclass
from enum import Enum, auto


class Severity(Enum):
    ERROR = auto()
    WARNING = auto()

@dataclass
class PlanProblem:
    severity: Severity
    message: str
