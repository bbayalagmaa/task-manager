"""JSON storage utilities for tasks."""

import json
import os
from datetime import datetime
from typing import List, Optional

from .models import Task

DEFAULT_FILE = "tasks.json"


def _get_path(filepath: str) -> str:
    return filepath


def load_tasks(filepath: str = DEFAULT_FILE) -> List[Task]:
    """Load all tasks from JSON file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        data = json.load(f)
    return [Task.from_dict(t) for t in data.get("tasks", [])]


def save_tasks(tasks: List[Task], filepath: str = DEFAULT_FILE) -> None:
    """Save all tasks to JSON file."""
    with open(filepath, "w") as f:
        json.dump({"tasks": [t.to_dict() for t in tasks]}, f, indent=2)


def _next_id(tasks: List[Task]) -> int:
    """Return next available task ID."""
    return max((t.id for t in tasks), default=0) + 1


def add_task(
    title: str,
    description: str = "",
    due_date: Optional[str] = None,
    priority: str = "medium",
    filepath: str = DEFAULT_FILE,
) -> Task:
    """Add a new task and persist it."""
    tasks = load_tasks(filepath)
    task = Task(
        id=_next_id(tasks),
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
    )
    tasks.append(task)
    save_tasks(tasks, filepath)
    return task


def update_task(task_id: int, filepath: str = DEFAULT_FILE, **kwargs) -> Optional[Task]:
    """Update fields on an existing task. Returns updated task or None if not found."""
    tasks = load_tasks(filepath)
    for task in tasks:
        if task.id == task_id:
            for key, value in kwargs.items():
                if hasattr(task, key) and value is not None:
                    setattr(task, key, value)
            task.updated_at = datetime.now().isoformat()
            save_tasks(tasks, filepath)
            return task
    return None


def delete_task(task_id: int, filepath: str = DEFAULT_FILE) -> bool:
    """Delete a task by ID. Returns True if deleted, False if not found."""
    tasks = load_tasks(filepath)
    original_count = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
    if len(tasks) == original_count:
        return False
    save_tasks(tasks, filepath)
    return True


def get_task(task_id: int, filepath: str = DEFAULT_FILE) -> Optional[Task]:
    """Get a single task by ID."""
    for task in load_tasks(filepath):
        if task.id == task_id:
            return task
    return None
