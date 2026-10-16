import json
import os
from dataclasses import asdict
from typing import Annotated

import requests
import typer
from dotenv import load_dotenv
from rich.console import Console
from typer import Typer

from ...models.task import PriorityType, Task

app = Typer()

load_dotenv()

console = Console()

BASE_URL = os.getenv("BACKEND_BASE_URL")


@app.command("add")
def add(
    name: Annotated[str, typer.Argument(help="Name of the Task")],
    description: Annotated[
        str | None, typer.Option("--description", "-d", help="Description of the Task")
    ] = None,
    priority: Annotated[
        PriorityType, typer.Option("--priority", "-p", help="Task Priority")
    ] = PriorityType.LOW,
):
    """
    Add Task
    """
    task = Task(title=name, description=description, priority=priority)
    headers = {"Content-Type": "application/json"}

    with console.status("[bold green]Adding Task...", spinner="dots"):
        response = requests.post(
            f"{BASE_URL}/tasks", data=json.dumps(asdict(task)), headers=headers
        )

    response.raise_for_status()

    if response.status_code == 201:
        typer.secho("Task added successfully!", fg=typer.colors.GREEN)
