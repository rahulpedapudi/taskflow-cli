from typer import Typer

app = Typer()


@app.command("delete")
def delete():
    """Delete a Task"""
