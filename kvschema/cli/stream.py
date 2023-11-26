import typer
from sys import stdout

app = typer.Typer(no_args_is_help=True)


@app.command("do")
def from_csv(src: str, dest: str = None):
    from kvschema.serializers import GeoDFSerializer

    if dest is None:
        dest = stdout

    obj = GeoDFSerializer.from_csv(src)
    GeoDFSerializer.to_jsonline(dest, obj)
