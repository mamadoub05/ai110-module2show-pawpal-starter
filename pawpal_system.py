from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from typing import List, Optional

FREQUENCY_DELTAS = {
    "daily": timedelta(days=1),
    "weekly": timedelta(days=7),
    "monthly": timedelta(days=30),
}


def _parse_time_to_minutes(time_str: str) -> Optional[int]:
    try:
        hours, minutes = time_str.split(":")
        return int(hours) * 60 + int(minutes)
    except (ValueError, AttributeError):
        return None


def _time_sort_key(time_str: str):
    minutes = _parse_time_to_minutes(time_str)
    return (minutes is None, minutes or 0)


@dataclass
class Task:
    """Represents a single activity (description, time, frequency, completion status)."""

    title: str
    time: str
    duration_minutes: int
    priority: str
    frequency: str
    completed: bool = False
    due_date: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> "Task":
        """Return a copy of this task reset for its next due date based on frequency."""
        delta = FREQUENCY_DELTAS.get(self.frequency)
        if delta is None or not self.due_date:
            return replace(self, completed=False)

        try:
            next_due_date = (datetime.strptime(self.due_date, "%Y-%m-%d") + delta).strftime("%Y-%m-%d")
        except ValueError:
            next_due_date = self.due_date

        return replace(self, completed=False, due_date=next_due_date)


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove any task with the given title from this pet's task list."""
        self.tasks = [task for task in self.tasks if task.title != title]

    def get_pending_tasks(self) -> List[Task]:
        """Return this pet's tasks that are not yet completed."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None


@dataclass
class Scheduler:
    """The "Brain" that retrieves, organizes, and manages tasks across pets."""

    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets managed by the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return the given tasks sorted chronologically by their time."""
        return sorted(tasks, key=lambda task: _time_sort_key(task.time))

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return the tasks belonging to the pet with the given name."""
        pet = self.owner.get_pet(pet_name)
        return list(pet.tasks) if pet else []

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return all tasks matching the given completion status."""
        return [task for task in self.get_all_tasks() if task.completed == completed]

    def detect_conflicts(self) -> List[str]:
        """Return descriptions of any tasks whose time windows overlap."""
        entries = [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if _parse_time_to_minutes(task.time) is not None
        ]

        conflicts = []
        for i in range(len(entries)):
            pet_a, task_a = entries[i]
            start_a = _parse_time_to_minutes(task_a.time)
            end_a = start_a + task_a.duration_minutes

            for j in range(i + 1, len(entries)):
                pet_b, task_b = entries[j]
                start_b = _parse_time_to_minutes(task_b.time)
                end_b = start_b + task_b.duration_minutes

                if start_a < end_b and start_b < end_a:
                    conflicts.append(
                        f"{pet_a.name} - {task_a.title} ({task_a.time}) conflicts with "
                        f"{pet_b.name} - {task_b.title} ({task_b.time})"
                    )

        return conflicts

    def mark_task_complete(self, pet_name: str, task_title: str) -> Optional[Task]:
        """Mark the named task for the named pet as complete, returning it if found."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return None

        for task in pet.tasks:
            if task.title == task_title:
                task.mark_complete()
                return task

        return None

    def build_daily_schedule(self) -> List[dict]:
        """Return every task across all pets as a time-sorted schedule of dicts."""
        entries = [
            {
                "pet": pet.name,
                "title": task.title,
                "time": task.time,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "completed": task.completed,
            }
            for pet in self.owner.pets
            for task in pet.tasks
        ]

        entries.sort(key=lambda entry: _time_sort_key(entry["time"]))
        return entries
