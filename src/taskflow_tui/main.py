from typing import ClassVar

from textual import on
from textual.app import App, ComposeResult
from textual.containers import (
    Horizontal,
    HorizontalGroup,
    HorizontalScroll,
    VerticalScroll,
)
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, Input, Label, Static

from ..api.tasks import add_task, get_tasks


class TaskMetricsCard(Widget):
    def __init__(self, title: str, content: str, variant: str = ""):
        super().__init__(classes=variant)
        self.title = title
        self.content = content

    def compose(self) -> ComposeResult:
        yield Static(self.title, classes="metric-title")
        yield Static(self.content, classes="metric-value")


class TaskItem(Widget):
    def __init__(
        self,
        todo_id: str,
        title: str,
        description: str,
        priority: str,
    ):
        super().__init__()
        self.todo_id = todo_id
        self.title = title
        self.description = description
        self.priority = priority

    def compose(self) -> ComposeResult:
        priority_class = self.priority.lower().replace(" ", "-")

        yield Horizontal(
            Label(f"#{self.todo_id}", classes="task-id"),
            Static(self.title, classes="task-title"),
            Static(self.description, classes="task-description"),
            Label(
                self.priority.upper(),
                classes=f"priority priority-{priority_class}",
            ),
            Button("Delete"),
            classes="task-row",
        )


class TaskFlowApp(App):
    """TaskFlow terminal dashboard."""

    CSS_PATH = "styles.tcss"
    BINDINGS: ClassVar = [
        ("r", "refresh_tasks", "Refresh"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(name="TASKFLOW", show_clock=True)
        yield Static("YOUR WORKSPACE / OVERVIEW", id="section-title")
        yield Static("Connecting to your task service...", id="status")
        yield HorizontalScroll(id="metrics")
        yield Input(placeholder="Call John...", id="todo_input")
        yield Button("Add Todo", id="submit-btn")
        yield Static("YOUR TASKS", id="tasks-heading")
        yield VerticalScroll(id="content")
        yield Footer()

    def on_mount(self) -> None:
        self.load_tasks()

    def load_tasks(self) -> None:
        status = self.query_one("#status", Static)
        metrics = self.query_one("#metrics", HorizontalScroll)
        content = self.query_one("#content", VerticalScroll)

        try:
            tasks = get_tasks()

            metrics.remove_children()
            content.remove_children()

            completed = sum(bool(getattr(task, "completed", False)) for task in tasks)
            active = len(tasks) - completed

            metrics.mount(TaskMetricsCard("TOTAL TASKS", str(len(tasks)), "total"))
            metrics.mount(TaskMetricsCard("ACTIVE", str(active), "active"))
            metrics.mount(TaskMetricsCard("COMPLETED", str(completed), "completed"))

            if not tasks:
                content.mount(
                    Static(
                        "No tasks yet. Your empty task list is suspiciously peaceful.",
                        classes="empty-state",
                    )
                )
            else:
                for task in tasks:
                    content.mount(
                        TaskItem(
                            str(task.id),
                            task.title,
                            task.description or "No description",
                            str(task.priority),
                        )
                    )

            status.update(f"  {len(tasks)} tasks loaded  /  API connected")

        except Exception as exc:
            status.update(f"  API ERROR: {exc}")

    def action_refresh_tasks(self) -> None:
        self.load_tasks()

    @on(Button.Pressed, "#submit-btn")
    def handle_submit(self) -> None:
        input_widget = self.query_one("#todo_input", Input)
        title = input_widget.value
        response = add_task(title=title, desc="")
        if response:
            self.load_tasks()
            input_widget.value = ""


if __name__ == "__main__":
    TaskFlowApp().run()
