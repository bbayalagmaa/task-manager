"""CLI entry point using Click."""

import click
from . import storage

PRIORITY_COLORS = {"high": "red", "medium": "yellow", "low": "green"}


def _format_task(t) -> str:
    """Return a colored string representation of a task."""
    color = PRIORITY_COLORS.get(t.priority, "white")
    checkbox = click.style("[x]", fg="bright_black") if t.status == "done" else click.style("[ ]", fg="cyan")
    task_id = click.style(f"#{t.id}", fg="bright_black")
    priority = click.style(f"[{t.priority}]", fg=color, bold=True)
    due = click.style(f" due {t.due_date}", fg="magenta") if t.due_date else ""
    title = click.style(t.title, fg="bright_black") if t.status == "done" else t.title
    return f"{checkbox} {task_id} {priority}{due}  {title}"


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
    click.echo(click.style("Added ", fg="green") + f"task #{task.id}: {task.title}")


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
        click.echo(click.style("No tasks found.", fg="bright_black"))
        return
    todo = [t for t in tasks if t.status == "todo"]
    done = [t for t in tasks if t.status == "done"]
    if todo:
        for t in todo:
            click.echo(_format_task(t))
    if done:
        if todo:
            click.echo()
        click.echo(click.style(f"  Completed ({len(done)})", fg="bright_black"))
        for t in done:
            click.echo(_format_task(t))


@cli.command()
@click.argument("task_id", type=int)
def done(task_id: int):
    """Mark a task as done."""
    task = storage.update_task(task_id, status="done")
    if task:
        click.echo(click.style("Done! ", fg="green") + f"#{task_id}: {task.title}")
    else:
        click.echo(click.style(f"Task #{task_id} not found.", fg="red"), err=True)


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id: int):
    """Delete a task."""
    if storage.delete_task(task_id):
        click.echo(click.style("Deleted ", fg="red") + f"task #{task_id}.")
    else:
        click.echo(click.style(f"Task #{task_id} not found.", fg="red"), err=True)


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
        click.echo(click.style("Updated ", fg="cyan") + f"task #{task_id}.")
    else:
        click.echo(click.style(f"Task #{task_id} not found.", fg="red"), err=True)


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
        click.echo(click.style("No matching tasks.", fg="bright_black"))
        return
    click.echo(click.style(f"  {len(results)} result(s) for ", fg="bright_black") + click.style(f'"{keyword}"', fg="cyan"))
    for t in results:
        click.echo(_format_task(t))


if __name__ == "__main__":
    cli()
