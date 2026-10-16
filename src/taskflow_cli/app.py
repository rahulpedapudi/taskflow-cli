from typer import Typer

from .commands.add import app as add_app
from .commands.delete import app as delete_app
from .commands.list import app as list_app

app = Typer(no_args_is_help=True)

app.add_typer(add_app)
app.add_typer(delete_app)
app.add_typer(list_app)


if __name__ == "__main__":
    app()
