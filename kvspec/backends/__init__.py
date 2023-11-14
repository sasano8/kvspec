from typing import Iterable, Tuple

from .abstract import KeyValueClient, WrapperClient, ReadOnlyClient, WriteOnlyClient
from .local import LocalStorageClient


class MockClient(KeyValueClient):
    def put_bytes(self, key, value: bytes):
        ...

    def get_substorage(self, relative_path):
        return self


class PrintClient(MockClient):
    def put_bytes(self, key, value: bytes):
        print(f"{key} {value}")


class ThreadSafeDictClient(KeyValueClient):
    def __init__(self, data: dict = None):
        import threading

        self.data = data or {}
        self.lock = threading.Lock()

    def put_bytes(self, key, value: bytes):
        if not isinstance(value, bytes):
            raise Exception()
        with self.lock:
            self.data[key] = value

    def get_bytes(self, key):
        with self.lock:
            return self.data[key]

    def put_bytes_stream(self, stream: Iterable[Tuple[str, bytes]]):
        with self.lock:
            for key, value in stream:
                if not isinstance(value, bytes):
                    raise Exception()
                self.data[key] = value
