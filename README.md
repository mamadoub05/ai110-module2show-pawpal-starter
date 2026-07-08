# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Features

- **Chronological sorting** — orders tasks by `HH:MM` time.
- **Pet-scoped filtering** — retrieves tasks for one named pet.
- **Status filtering** — toggles between pending and completed tasks.
- **Pending-task lookup** — returns a pet's incomplete tasks directly.
- **Conflict warnings** — flags tasks scheduled at the exact same time across pets.
- **Daily & weekly recurrence** — generates the next occurrence of a recurring task; one-time tasks don't recur.
- **Auto-recurrence on completion** — completing a recurring task automatically schedules and re-adds its next occurrence.
- **Daily schedule builder** — aggregates every pet's pending tasks into one time-sorted, display-ready schedule.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## 🖥️ Sample Output

```
==================================================
  PawPal+ Daily Schedule for Jordan
==================================================
  08:00  [Mochi]  Feeding  (10 min)  priority: high
  08:00  [Biscuit]  Morning Walk  (30 min)  priority: high
  09:00  [Biscuit]  Feeding  (10 min)  priority: high
  12:00  [Mochi]  Litter Box  (5 min)  priority: medium
  15:00  [Mochi]  Grooming  (20 min)  priority: low
  18:00  [Biscuit]  Medication  (5 min)  priority: high

--- Conflict Check ---
Mochi - Feeding (08:00) conflicts with Biscuit - Morning Walk (08:00)

--- Biscuit's Tasks Only ---
  08:00  Morning Walk
  09:00  Feeding
  18:00  Medication

--- Marking Biscuit's Morning Walk complete ---
  Next occurrence created: Morning Walk on 2026-07-07

Done.
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

Test output:

```
============================= test session starts ==============================
collected 11 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED
tests/test_pawpal.py::test_completed_task_not_in_pending PASSED
tests/test_pawpal.py::test_add_task_increases_count PASSED
tests/test_pawpal.py::test_sort_by_time_is_chronological PASSED
tests/test_pawpal.py::test_sort_handles_single_task PASSED
tests/test_pawpal.py::test_conflict_detected_same_time PASSED
tests/test_pawpal.py::test_no_conflict_different_times PASSED
tests/test_pawpal.py::test_daily_task_creates_next_occurrence PASSED
tests/test_pawpal.py::test_once_task_does_not_recur PASSED
tests/test_pawpal.py::test_filter_by_pet_returns_correct_tasks PASSED
tests/test_pawpal.py::test_filter_by_status_pending PASSED

============================== 11 passed in 0.03s ==============================
```
My confidence level is a 4

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Chronological sorting | Scheduler.sort_by_time() | Sorts by HH:MM string, chronological order; defaults to the full task list when none is passed |
| Pet-scoped filtering | Scheduler.filter_by_pet() | Returns tasks for one named pet (case-insensitive lookup via Owner.get_pet()) |
| Status filtering | Scheduler.filter_by_status() | Toggle between pending and completed, defaults to pending |
| Pending-task lookup | Pet.get_pending_tasks() | Returns a pet's incomplete tasks directly, without going through the Scheduler |
| Conflict warnings | Scheduler.detect_conflicts() | Exact time-match check across all pets, returns warning strings |
| Daily & weekly recurrence | Task.next_occurrence() | Builds the next Task using timedelta for "daily"/"weekly"; "once" tasks return None |
| Auto-recurrence on completion | Scheduler.mark_task_complete() | Marks a task done, then creates and re-adds its next occurrence to the pet's task list |
| Daily schedule builder | Scheduler.build_daily_schedule() | Aggregates every pet's pending tasks into one time-sorted, display-ready list |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:
1. Enter your name and click Set Owner to initialize the app.
2. Add a pet by entering its name, species, and age, then click Add Pet.
3. Add tasks to your pet — set a title, time (HH:MM), duration, priority, and frequency.
4. Click Generate Schedule to see today's sorted plan. Any time conflicts appear as yellow warnings above the table.
5. Use the Mark Task Complete section to check off a task. Daily and weekly tasks automatically generate their next occurrence.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
