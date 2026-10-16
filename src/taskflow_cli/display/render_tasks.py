from rich.console import Console
from rich.table import Table

from ..models.task import Task


def render_tasks(tasks: list[Task], console: Console):
    table = Table(title="Your Tasks")

    table.add_column("ID", style="dim")
    table.add_column("Status")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Priority")

    for t in tasks:
        table.add_row(
            str(t.id),
            "✓" if t.completed else "×",
            t.title,
            t.description or " - ",
            t.priority,
        )

    console.print(table)
