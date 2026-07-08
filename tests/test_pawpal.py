import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler

TODAY = datetime.today().strftime("%Y-%m-%d")


def make_scheduler():
    """Helper: build a standard owner/pet/scheduler for tests."""
    owner = Owner("Jordan")
    dog = Pet("Biscuit", "dog", 5)
    cat = Pet("Mochi", "cat", 3)
    dog.add_task(Task("Morning Walk", "08:00", 30, "high",   "daily",  due_date=TODAY))
    dog.add_task(Task("Feeding",      "09:00", 10, "high",   "daily",  due_date=TODAY))
    dog.add_task(Task("Medication",   "18:00", 5,  "high",   "daily",  due_date=TODAY))
    cat.add_task(Task("Feeding",      "08:00", 10, "high",   "daily",  due_date=TODAY))
    cat.add_task(Task("Litter Box",   "12:00", 5,  "medium", "daily",  due_date=TODAY))
    owner.add_pet(dog)
    owner.add_pet(cat)
    return Scheduler(owner)


# ── Task Completion ──────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    """Marking a task complete should set completed=True."""
    task = Task("Walk", "08:00", 30, "high", "once", due_date=TODAY)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_completed_task_not_in_pending():
    """A completed task should not appear in get_pending_tasks."""
    pet = Pet("Rex", "dog", 2)
    task = Task("Walk", "08:00", 30, "high", "once", due_date=TODAY)
    pet.add_task(task)
    task.mark_complete()
    assert task not in pet.get_pending_tasks()


# ── Task Addition ────────────────────────────────────────────────────────────

def test_add_task_increases_count():
    """Adding a task to a pet should increase its task count."""
    pet = Pet("Rex", "dog", 2)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "08:00", 30, "high", "once", due_date=TODAY))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Feeding", "09:00", 10, "high", "daily", due_date=TODAY))
    assert len(pet.tasks) == 2


# ── Sorting ──────────────────────────────────────────────────────────────────

def test_sort_by_time_is_chronological():
    """Tasks should be returned in HH:MM order."""
    scheduler = make_scheduler()
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_sort_handles_single_task():
    """Sorting a single task should not crash."""
    owner = Owner("Alex")
    pet = Pet("Solo", "cat", 1)
    pet.add_task(Task("Feeding", "10:00", 10, "medium", "daily", due_date=TODAY))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    result = scheduler.sort_by_time()
    assert len(result) == 1


# ── Conflict Detection ───────────────────────────────────────────────────────

def test_conflict_detected_same_time():
    """Two tasks at the same time should trigger a conflict warning."""
    scheduler = make_scheduler()
    conflicts = scheduler.detect_conflicts()
    # Both Biscuit and Mochi have tasks at 08:00
    assert len(conflicts) > 0
    assert "08:00" in conflicts[0]


def test_no_conflict_different_times():
    """Tasks at different times should not trigger any warnings."""
    owner = Owner("Sam")
    pet = Pet("Buddy", "dog", 3)
    pet.add_task(Task("Walk",    "07:00", 30, "high",   "daily", due_date=TODAY))
    pet.add_task(Task("Feeding", "09:00", 10, "high",   "daily", due_date=TODAY))
    pet.add_task(Task("Meds",    "18:00", 5,  "medium", "daily", due_date=TODAY))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


# ── Recurring Tasks ──────────────────────────────────────────────────────────

def test_daily_task_creates_next_occurrence():
    """Completing a daily task should create a new task for the next day."""
    scheduler = make_scheduler()
    new_task = scheduler.mark_task_complete("Biscuit", "Morning Walk")
    assert new_task is not None
    assert new_task.completed is False
    assert new_task.title == "Morning Walk"


def test_once_task_does_not_recur():
    """A one-time task should not create a next occurrence."""
    task = Task("Vet Visit", "10:00", 60, "high", "once", due_date=TODAY)
    assert task.next_occurrence() is None


# ── Filtering ────────────────────────────────────────────────────────────────

def test_filter_by_pet_returns_correct_tasks():
    """Filtering by pet name should return only that pet's tasks."""
    scheduler = make_scheduler()
    tasks = scheduler.filter_by_pet("Biscuit")
    assert len(tasks) == 3
    titles = [t.title for t in tasks]
    assert "Morning Walk" in titles


def test_filter_by_status_pending():
    """filter_by_status(False) should return only incomplete tasks."""
    scheduler = make_scheduler()
    pending = scheduler.filter_by_status(completed=False)
    assert all(not t.completed for t in pending)