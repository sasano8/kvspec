import typer
from sys import stdout
from typing import Literal, NamedTuple
import time

app = typer.Typer(no_args_is_help=True)


MEDIA_TYPES = [
    "application/json",
    "application/x-ndjson",
    "text/csv",
]


class MediaType:
    def __init__(self, alias, media_type):
        ...


{
    ".txt": "text/plain",
    ".html": "text/html",
    ".csv": "text/csv",
    ".xml": "application/xml",
    ".json": "application/json",
    ".geo+json": "application/geo+json",
    ".jsonl": "application/x-ndjson",
    ".geo+jsonl": "application/geo+x-ndjson",
    ".parquet": "application/parquet",
    ".geo+parquet": "application/geo+parquet",
    ".vtable": "application/json",
}

vdb = {"type": "postgres", "schema": "public", "table": "users"}


@app.command()
# def from_csv(src: str, dest: str = None, serializer: Literal["jsonl", "ndjson", "csv"] = "jsonl"):
def from_csv(
    src: str,
    dest: str = None,
    serializer: str = "jsonl",
    interval: int = None,
    loop: bool = False,
):
    from kvschema.serializers import GeoDFSerializer

    if dest is None:
        dest = stdout

    obj = GeoDFSerializer.from_csv(src)

    if serializer == "jsonl":
        GeoDFSerializer.to_jsonline(dest, obj)
    elif serializer == "csv":
        GeoDFSerializer.to_csv(dest, obj)
    else:
        raise Exception()


class FileStream:
    def __init__(self, media_type):
        self.media_type = media_type
        self.buffer = []

    def readlines(self):
        return self.buffer.readlines()
