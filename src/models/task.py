from dataclasses import dataclass, field
from enum import Enum


class PriorityType(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    title: str
    id: int | None = None
    description: str | None = None
    priority: PriorityType = field(default=PriorityType.LOW)
    completed: bool = field(default=False)
