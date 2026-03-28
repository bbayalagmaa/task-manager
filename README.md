# Task Manager CLI

A command-line task manager built with Python and Click. Supports priorities, due dates, filtering, and search — all stored locally in JSON.

## Setup

**Requirements:** Python 3.8+

```bash
# Install dependencies
pip install -e .
```

## Usage

```bash
task <command> [options]
```

### Add a task

```bash
task add "Buy groceries"
task add "Study for exam" --priority high --due 2026-04-10
task add "Read chapter 5" -p high -d "Chapter 5 of stats textbook"
```

### List tasks

```bash
task list                        # all tasks
task list --status todo          # only incomplete
task list --status done          # only completed
task list --priority high        # filter by priority
```

### Complete a task

```bash
task done 3                      # mark task #3 as done
```

### Delete a task

```bash
task delete 2                    # remove task #2
```

### Edit a task

```bash
task edit 1 --title "New title"
task edit 1 --priority low --due 2026-05-01
```

### Search

```bash
task search "exam"               # search titles and descriptions
```

## Example session

```
$ task add "Finish project report" -p high --due 2026-04-15
Added task #1: Finish project report

$ task add "Buy coffee"
Added task #2: Buy coffee

$ task add "Reply to emails" -p low
Added task #3: Reply to emails

$ task list
[ ] #1 [high] (due 2026-04-15) Finish project report
[ ] #2 [medium] Buy coffee
[ ] #3 [low] Reply to emails

$ task done 2
Marked #2 as done.

$ task list --status todo
[ ] #1 [high] (due 2026-04-15) Finish project report
[ ] #3 [low] Reply to emails

$ task delete 3
Deleted task #3.
```

## Data storage

Tasks are saved to `tasks.json` in the directory where you run the command.

## Running tests

```bash
pytest
```

## Dependencies

- [Click](https://click.palletsprojects.com/) — CLI framework
- [pytest](https://pytest.org/) — testing
