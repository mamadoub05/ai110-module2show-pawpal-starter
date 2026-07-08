import streamlit as st
from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Your smart pet care planner.")

TODAY = datetime.today().strftime("%Y-%m-%d")

# Session State Init

if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# Owner Setup 

st.subheader("👤 Owner Info")
owner_name = st.text_input("Your name", value="Jordan")

if st.button("Set Owner"):
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.scheduler = Scheduler(st.session_state.owner)
    st.success(f"Welcome, {owner_name}!")

if st.session_state.owner is None:
    st.info("Set your name above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

# Add a Pet 

st.divider()
st.subheader("🐶 Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Biscuit")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    existing = owner.get_pet(pet_name)
    if existing:
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, age=age))
        st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.caption("Your pets: " + ", ".join(p.name for p in owner.pets))

# Add a Task 

st.divider()
st.subheader("📋 Add a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    col1, col2 = st.columns(2)
    with col1:
        task_pet = st.selectbox("Pet", [p.name for p in owner.pets])
        task_title = st.text_input("Task title", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col2:
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        pet = owner.get_pet(task_pet)
        if pet:
            pet.add_task(Task(
                title=task_title,
                time=task_time,
                duration_minutes=task_duration,
                priority=task_priority,
                frequency=task_frequency,
                due_date=TODAY,
            ))
            st.success(f"Added '{task_title}' to {task_pet}'s schedule.")

# Daily Schedule

st.divider()
st.subheader("📅 Today's Schedule")

if st.button("Generate Schedule"):
    schedule = scheduler.build_daily_schedule()
    conflicts = scheduler.detect_conflicts()

    if conflicts:
        for warning in conflicts:
            st.warning(warning)

    if not schedule:
        st.info("No pending tasks. Add tasks above.")
    else:
        st.table(schedule)

# Mark Task Complete 

st.divider()
st.subheader("✅ Mark Task Complete")

if owner.pets:
    col1, col2 = st.columns(2)
    with col1:
        complete_pet = st.selectbox("Pet", [p.name for p in owner.pets], key="complete_pet")
    with col2:
        pet_obj = owner.get_pet(complete_pet)
        pending = [t.title for t in pet_obj.get_pending_tasks()] if pet_obj else []
        complete_task = st.selectbox("Task", pending if pending else ["(no pending tasks)"])

    if st.button("Mark Complete") and pending:
        new_task = scheduler.mark_task_complete(complete_pet, complete_task)
        st.success(f"'{complete_task}' marked complete!")
        if new_task:
            st.info(f"Next occurrence scheduled: {new_task.title} on {new_task.due_date}")

st.divider()
st.caption("PawPal+ — built with Python + Streamlit.")
