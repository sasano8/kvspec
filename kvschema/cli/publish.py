import json
from sys import stdout, stdin
import sys

import typer
from time import sleep


app = typer.Typer(no_args_is_help=True)


@app.command()
def from_stdin(dest: str = "-"):
    from kvschema.serializers import GeoDFSerializer

    _src = stdin

    if dest == "-" or dest == "stdout://":
        _dest = stdout
    else:
        raise Exception()

    # TODO: 空行を受け取った時の処理

    # 対話的に入力を受け付けとるか、パイプやリダイレクトで入力を受け取るか
    if sys.stdin.isatty():
        while True:
            try:
                line = input()
                _dest.write(line)
                print()
            except EOFError:
                break
    else:
        for row in _src.readlines():
            _dest.write(row)
