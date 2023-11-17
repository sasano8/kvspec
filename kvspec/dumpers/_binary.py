from .abstract import DumperBase


class BinaryDumper(DumperBase):
    content_type = "application/octet-stream"

    def __iter__(self):
        return iter(self.it)
