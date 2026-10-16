import os

import requests
from dotenv import load_dotenv
from rich.console import Console
from typer import Typer

from ..display.render_tasks import render_tasks
from ..models.task import Task

app = Typer()
load_dotenv()

BASE_URL = os.getenv("BACKEND_BASE_URL")

console = Console()


@app.command("list")
def list_tasks():
    """Lists all the tasks"""
    headers = {"Content-Type": "application/json"}

    with console.status("[bold green]Adding Task...", spinner="dots"):
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)

    response.raise_for_status()

    # converting dictionaries into Task Objects
    tasks = [Task(**item) for item in response.json()]
    render_tasks(tasks, console)
