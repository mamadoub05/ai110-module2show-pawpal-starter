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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The conflict detection only flags tasks that share an exact time string rather than checking for overlapping time windows. For example, a 30-minute walk starting at 08:00 and a 10-minute feeding starting at 08:15 would not be flagged even though they overlap in real time. This tradeoff is reasonable for a daily planning tool used by a single owner because exact-time conflicts are the most common mistake, and checking duration overlap would require more complex interval arithmetic that adds complexity without much benefit for this use case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
