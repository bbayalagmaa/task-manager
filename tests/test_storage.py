"""Tests for storage utilities."""

import os
import pytest
from src.storage import add_task, load_tasks, save_tasks, update_task, delete_task, get_task
from src.models import Task


@pytest.fixture
def tmp_file(tmp_path):
    return str(tmp_path / "tasks.json")


def test_load_tasks_empty(tmp_file):
    tasks = load_tasks(tmp_file)
    assert tasks == []


def test_add_task(tmp_file):
    task = add_task("Buy milk", filepath=tmp_file)
    assert task.id == 1
    assert task.title == "Buy milk"
    assert task.status == "todo"
    assert task.priority == "medium"


def test_add_multiple_tasks_increments_id(tmp_file):
    t1 = add_task("First", filepath=tmp_file)
    t2 = add_task("Second", filepath=tmp_file)
    assert t1.id == 1
    assert t2.id == 2


def test_add_task_persists(tmp_file):
    add_task("Persisted task", filepath=tmp_file)
    tasks = load_tasks(tmp_file)
    assert len(tasks) == 1
    assert tasks[0].title == "Persisted task"


def test_add_task_with_all_fields(tmp_file):
    task = add_task(
        "Study", description="Read chapter 5", due_date="2026-03-20", priority="high", filepath=tmp_file
    )
    assert task.description == "Read chapter 5"
    assert task.due_date == "2026-03-20"
    assert task.priority == "high"


def test_update_task_status(tmp_file):
    add_task("Task A", filepath=tmp_file)
    updated = update_task(1, filepath=tmp_file, status="done")
    assert updated is not None
    assert updated.status == "done"


def test_update_task_not_found(tmp_file):
    result = update_task(99, filepath=tmp_file, status="done")
    assert result is None


def test_delete_task(tmp_file):
    add_task("Delete me", filepath=tmp_file)
    result = delete_task(1, filepath=tmp_file)
    assert result is True
    assert load_tasks(tmp_file) == []


def test_delete_task_not_found(tmp_file):
    result = delete_task(99, filepath=tmp_file)
    assert result is False


def test_get_task(tmp_file):
    add_task("Get me", filepath=tmp_file)
    task = get_task(1, filepath=tmp_file)
    assert task is not None
    assert task.title == "Get me"


def test_get_task_not_found(tmp_file):
    assert get_task(99, tmp_file) is None


def test_task_to_dict_and_from_dict():
    task = Task(id=1, title="Round trip", priority="low")
    d = task.to_dict()
    restored = Task.from_dict(d)
    assert restored.id == task.id
    assert restored.title == task.title
    assert restored.priority == task.priority
