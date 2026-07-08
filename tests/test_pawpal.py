from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(
        title="Feeding",
        time="08:00",
        duration_minutes=10,
        priority="high",
        frequency="daily",
    )
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="cat", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(
        Task(
            title="Grooming",
            time="15:00",
            duration_minutes=20,
            priority="low",
            frequency="weekly",
        )
    )

    assert len(pet.tasks) == 1
