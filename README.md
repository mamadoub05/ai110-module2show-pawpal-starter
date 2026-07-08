# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time() | Sorts by HH:MM string, chronological order|
| Filtering by pet | Scheduler.filter_by_pet()| Returns tasks for one named pet |
| Filtering by status | Scheduler.filter_by_status()| Toggle between pending and completed|
| Conflict detection | Scheduler.detect_conflicts()| Exact time-match check, returns warning strings |
| Recurring tasks|Task.next_occurrence() + Scheduler.mark_task_complete() | Uses timedelta for daily/weekly scheduling|
 
## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
