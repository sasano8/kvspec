import typer

from .subscribe import app as subscribe_app, from_csv
from .publish import app as publish_app, from_stdin

app = typer.Typer(no_args_is_help=True)
# app.add_typer(subscribe_app, name="subscribe")
# app.add_typer(publish_app, name="publish")

app.command("subscribe")(from_csv)
app.command("publish")(from_stdin)
app.command("transfer")(lambda: None)  # その他命名候補: load
app.command("inspect")(lambda: None)
