"""
PawPal+ backend logic.
Four classes: Task, Pet, Owner, Scheduler.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    time: str          # "HH:MM" format
    duration_minutes: int
    priority: str      # "low", "medium", "high"
    frequency: str     # "once", "daily", "weekly"
    completed: bool = False
    due_date: str = ""  # "YYYY-MM-DD", used for recurring tasks

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next occurrence if recurring."""
        if self.frequency == "once":
            return None

        base = datetime.strptime(self.due_date, "%Y-%m-%d") if self.due_date else datetime.today()

        if self.frequency == "daily":
            next_date = base + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = base + timedelta(weeks=1)
        else:
            return None

        return Task(
            title=self.title,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
            due_date=next_date.strftime("%Y-%m-%d"),
        )


@dataclass
class Pet:
    """Stores pet info and its list of tasks."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str):
        """Remove a task by title."""
        self.tasks = [t for t in self.tasks if t.title != title]

    def get_pending_tasks(self) -> List[Task]:
        """Return only incomplete tasks."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """Manages an owner's profile and their pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pet(self, name: str) -> Optional[Pet]:
        """Look up a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


class Scheduler:
    """The brain — retrieves, sorts, filters, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks chronologically by their time field (HH:MM)."""
        tasks = tasks if tasks is not None else self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to a specific pet."""
        pet = self.owner.get_pet(pet_name)
        if not pet:
            return []
        return pet.tasks

    def filter_by_status(self, completed: bool = False) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [t for t in self.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self) -> List[str]:
        """
        Check for tasks scheduled at the exact same time.
        Returns a list of warning strings, empty if no conflicts.
        """
        warnings = []
        tasks = self.get_all_tasks()
        seen = {}
        for task in tasks:
            if task.time in seen:
                warnings.append(
                    f"⚠️ Conflict at {task.time}: '{seen[task.time]}' and '{task.title}' overlap."
                )
            else:
                seen[task.time] = task.title
        return warnings

    def mark_task_complete(self, pet_name: str, task_title: str) -> Optional[Task]:
        """
        Mark a task complete and auto-create next occurrence if recurring.
        Returns the new Task if one was created, else None.
        """
        pet = self.owner.get_pet(pet_name)
        if not pet:
            return None

        for task in pet.tasks:
            if task.title == task_title and not task.completed:
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task:
                    pet.add_task(next_task)
                return next_task

        return None

    def build_daily_schedule(self) -> List[dict]:
        """
        Build a sorted daily schedule of pending tasks with pet labels.
        Returns list of dicts for easy display.
        """
        schedule = []
        for pet in self.owner.pets:
            for task in pet.get_pending_tasks():
                schedule.append({
                    "time": task.time,
                    "pet": pet.name,
                    "task": task.title,
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                    "frequency": task.frequency,
                })
        schedule.sort(key=lambda x: x["time"])
        return schedule