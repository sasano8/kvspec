from .abstract import DumperBase

from kvspec.registry import builtins


@builtins.dumper
class BinaryDumper(DumperBase):
    content_type = "application/octet-stream"

    def __iter__(self):
        return iter(self.it)
