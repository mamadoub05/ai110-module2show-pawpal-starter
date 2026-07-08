from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    title: str
    time: str
    duration_minutes: int
    priority: str
    frequency: str
    completed: bool = False
    due_date: str = ""

    def mark_complete(self) -> None:
        pass

    def next_occurrence(self) -> "Task":
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def get_pending_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass

    def get_pet(self, name: str) -> Optional[Pet]:
        pass


@dataclass
class Scheduler:
    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        pass

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        pass

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        pass

    def filter_by_status(self, completed: bool) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[str]:
        pass

    def mark_task_complete(self, pet_name: str, task_title: str) -> Optional[Task]:
        pass

    def build_daily_schedule(self) -> List[dict]:
        pass
