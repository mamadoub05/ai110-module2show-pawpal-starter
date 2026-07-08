# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
a. Initial design

I designed four classes that are Task, Pet, Owner, and Scheduler. Task holds everything about a single activity from its title, scheduled time, duration, priority, frequency, and completion status. Pet stores the animal's basic info and owns a list of Tasks. Owner manages multiple pets and acts as the top-level entry point for all data. Scheduler is the brain so it takes an Owner and provides methods for sorting, filtering, conflict detection, and building the daily plan. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
My initial design had the Scheduler holding a flat list of tasks directly, but I changed it so the Scheduler always pulls tasks through the Owner → Pet → Task chain. This keeps data ownership clear so the Pet is always the source of truth for its own tasks, and the Scheduler is just a query layer on top.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers time, priority level, and frequency . Tasks are sorted chronologically so the owner sees the day in order. Priority is stored as metadata and displayed so the owner can visually identify what matters most. I decided time order was the most important constraint since a pet care schedule is fundamentally time-driven.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The conflict detection only flags tasks that share an exact time string rather than checking for overlapping time windows. For example, a 30-minute walk starting at 08:00 and a 10-minute feeding starting at 08:15 would not be flagged even though they overlap in real time. This tradeoff is reasonable for a daily planning tool used by a single owner because exact-time conflicts are the most common mistake, and checking duration overlap would require more complex interval arithmetic that adds complexity without much benefit for this use case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used the Claude agent for generating class skeletons, implementing sorting and conflict detection, and creating the pytest suite. The most helpful prompts were specific and scoped to one file at a time, like "move check_guess into logic_utils.py and fix the swapped messages." Asking Claude to explain logic step-by-step before applying it helped me understand what the code was doing rather than just copying it too.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The claude agent initially suggested using a flat list of tasks in the Scheduler rather than routing through Owner → Pet. I rejected this because it would break the ownership model because if the Scheduler held its own copy of tasks, updates made through Pet.add_task() wouldn't be reflected in the schedule. I verified the correct approach by tracing the data flow manually and confirming that Scheduler always reads live from owner.pets.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion, task addition, sorting correctness, conflict detection , recurring task logic, and pet filtering. These tests cover the core behaviors that the scheduler depends on because if any of these break, the daily schedule would be wrong.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm confident in the core logic sinnce all 11 tests passed and the CLI demo produces a correct, readable schedule. Edge cases I'd test next with more time are a pet with zero tasks, an owner with zero pets, tasks with invalid time formats like "25:99", and what happens when mark_task_complete is called on a task that doesn't exist.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The separation between the logic layer and the UI  worked really well. Because all the logic was tested in isolation through main.py and pytest before I touched Streamlit so, wiring the UI was straightforward. I just called the methods I'd already verified which made debugging much easier.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

 I'd add a priority-based scheduling mode where the Scheduler automatically picks which tasks to include if the owner only has a limited number of hours in the day, rather than showing all tasks unconditionally.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that AI is most useful when you give it a clear, scoped task. This allows me to keep the design in my own hands and only use AI to execute specific pieces. It also means I'm always able to understand what the code was doing and could catch mistakes before they compounded.