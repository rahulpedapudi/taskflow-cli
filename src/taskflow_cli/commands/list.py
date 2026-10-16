import os

from dotenv import load_dotenv
from rich.console import Console
from typer import Typer

from ...api.tasks import get_tasks
from ..display.render_tasks import render_tasks

app = Typer()
load_dotenv()

BASE_URL = os.getenv("BACKEND_BASE_URL")

console = Console()


@app.command("list")
def list_tasks():
    """Lists all the tasks"""

    with console.status("[bold green]Adding Task...", spinner="dots"):
        tasks = get_tasks()
    render_tasks(tasks, console)
