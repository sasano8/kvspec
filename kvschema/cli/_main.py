import typer

from .stream import app as loader_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(loader_app, name="stream")
