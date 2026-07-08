from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="cat", age=3)
biscuit = Pet(name="Biscuit", species="dog", age=5)

# Tasks for Mochi
mochi.add_task(Task("Feeding",       time="08:00", duration_minutes=10, priority="high",   frequency="daily",  due_date=datetime.today().strftime("%Y-%m-%d")))
mochi.add_task(Task("Litter Box",    time="12:00", duration_minutes=5,  priority="medium", frequency="daily",  due_date=datetime.today().strftime("%Y-%m-%d")))
mochi.add_task(Task("Grooming",      time="15:00", duration_minutes=20, priority="low",    frequency="weekly", due_date=datetime.today().strftime("%Y-%m-%d")))

# Tasks for Biscuit (intentional conflict at 08:00 to demo detection)
biscuit.add_task(Task("Morning Walk", time="08:00", duration_minutes=30, priority="high",   frequency="daily",  due_date=datetime.today().strftime("%Y-%m-%d")))
biscuit.add_task(Task("Feeding",      time="09:00", duration_minutes=10, priority="high",   frequency="daily",  due_date=datetime.today().strftime("%Y-%m-%d")))
biscuit.add_task(Task("Medication",   time="18:00", duration_minutes=5,  priority="high",   frequency="daily",  due_date=datetime.today().strftime("%Y-%m-%d")))

owner.add_pet(mochi)
owner.add_pet(biscuit)

scheduler = Scheduler(owner)


print("=" * 50)
print(f"  PawPal+ Daily Schedule for {owner.name}")
print("=" * 50)

schedule = scheduler.build_daily_schedule()
for entry in schedule:
  print(f"  {entry['time']}  [{entry['pet']}]  {entry['title']}  ({entry['duration_minutes']} min)  priority: {entry['priority']}")
# Conflict Detection 

print("\n--- Conflict Check ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts detected.")

#Filtering Demo 

print("\n--- Biscuit's Tasks Only ---")
for task in scheduler.filter_by_pet("Biscuit"):
    print(f"  {task.time}  {task.title}")

#  Recurring Task Demo 

print("\n--- Marking Biscuit's Morning Walk complete ---")
new_task = scheduler.mark_task_complete("Biscuit", "Morning Walk")
if new_task:
    print(f"  Next occurrence created: {new_task.title} on {new_task.due_date}")

print("\nDone.")