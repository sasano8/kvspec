from json import dumps as dump_json

from .abstract import DumperBase

from kvspec.registry import builtins


@builtins.dumper
class JsonlineDumper(DumperBase):
    content_type = "application/jsonlines"

    def __iter__(self):
        for row in self.it:
            yield dump_json(row, ensure_ascii=False)
            yield "\n"
