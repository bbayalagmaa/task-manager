"""CLI entry point using Click."""

import click
from . import storage


@click.group()
def cli():
    """Personal task manager."""
    pass


@cli.command()
@click.argument("title")
@click.option("--description", "-d", default="", help="Task description")
@click.option("--due", default=None, help="Due date (YYYY-MM-DD)")
@click.option(
    "--priority", "-p",
    default="medium",
    type=click.Choice(["high", "medium", "low"]),
    help="Priority level",
)
def add(title: str, description: str, due: str, priority: str):
    """Add a new task."""
    task = storage.add_task(title, description, due, priority)
    click.echo(f"Added task #{task.id}: {task.title}")


@cli.command("list")
@click.option("--status", default=None, type=click.Choice(["todo", "done"]))
@click.option("--priority", default=None, type=click.Choice(["high", "medium", "low"]))
def list_tasks(status: str, priority: str):
    """List tasks."""
    tasks = storage.load_tasks()
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if not tasks:
        click.echo("No tasks found.")
        return
    for t in tasks:
        due = f" (due {t.due_date})" if t.due_date else ""
        done = "[x]" if t.status == "done" else "[ ]"
        click.echo(f"{done} #{t.id} [{t.priority}]{due} {t.title}")


@cli.command()
@click.argument("task_id", type=int)
def done(task_id: int):
    """Mark a task as done."""
    task = storage.update_task(task_id, status="done")
    if task:
        click.echo(f"Marked #{task_id} as done.")
    else:
        click.echo(f"Task #{task_id} not found.", err=True)


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id: int):
    """Delete a task."""
    if storage.delete_task(task_id):
        click.echo(f"Deleted task #{task_id}.")
    else:
        click.echo(f"Task #{task_id} not found.", err=True)


@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", default=None)
@click.option("--description", "-d", default=None)
@click.option("--due", default=None)
@click.option("--priority", "-p", default=None, type=click.Choice(["high", "medium", "low"]))
def edit(task_id: int, title: str, description: str, due: str, priority: str):
    """Edit a task."""
    task = storage.update_task(
        task_id, title=title, description=description, due_date=due, priority=priority
    )
    if task:
        click.echo(f"Updated task #{task_id}.")
    else:
        click.echo(f"Task #{task_id} not found.", err=True)


@cli.command()
@click.argument("keyword")
def search(keyword: str):
    """Search tasks by keyword."""
    tasks = storage.load_tasks()
    kw = keyword.lower()
    results = [
        t for t in tasks
        if kw in t.title.lower() or kw in t.description.lower()
    ]
    if not results:
        click.echo("No matching tasks.")
        return
    for t in results:
        due = f" (due {t.due_date})" if t.due_date else ""
        done = "[x]" if t.status == "done" else "[ ]"
        click.echo(f"{done} #{t.id} [{t.priority}]{due} {t.title}")


if __name__ == "__main__":
    cli()
