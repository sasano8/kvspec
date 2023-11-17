from urllib.parse import SplitResult as ParsedUrl
from typing import Union

from kvspec.dumpers import JsonlineDumper


class FileLoader:
    schema = ["abs", "relative"]

    def __init__(self, backend):
        self.backend = backend

    @classmethod
    def check_schema(cls, value):
        if isinstance(cls.schema, set):
            return value in cls.schema
        else:
            return value == cls.schema

    @classmethod
    def load(
        cls,
        registry,
        url_or_spec: Union[ParsedUrl, str],
        loader: dict = {},
        select: dict = {},
        dumper: dict = {},
    ):
        from kvspec.backends.local import LocalStorageClient
        from kvspec.loaders.functions import csv_to_dict, parse_file_url

        path = parse_file_url(url_or_spec)
        backend = LocalStorageClient(path)

        if loader["type"] == "csv_to_dict":
            it = csv_to_dict(backend, header=loader.get("header", True))
        else:
            raise NotImplementedError()

        ctype = dumper["content-type"]
        if ctype == "application/jsonlines":
            _dumper = JsonlineDumper(it)
            return _dumper
        else:
            raise NotImplementedError()

    @classmethod
    def _build(cls):
        ...
