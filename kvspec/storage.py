from typing import Iterable, Tuple
from abc import ABC, abstractmethod


class KeyValueClient(ABC):
    @abstractmethod
    def get_substorage(self, relative_path):
        raise NotImplementedError()
    
    def as_readonly(self):
        return ReadOnlyClient(self)

    def as_writeonly(self):
        return WriteOnlyClient(self)

    def get_bytes(self, key) -> bytes:
        raise NotImplementedError()

    def put_bytes(self, key, value: bytes):
        raise NotImplementedError()
    
    def put_bytes_stream(self, stream: Iterable[Tuple[str, bytes]]):
        for key, value in stream:
            self.put_bytes(key, value)


class MockClient(KeyValueClient):
    def put_bytes(self, key, value: bytes):
        ...
        
    def get_substorage(self, relative_path):
        return self


class PrintClient(MockClient):
    def put_bytes(self, key, value: bytes):
        print(f"{key} {value}")


class WrapperClient(KeyValueClient):
    def __init__(self, client: KeyValueClient):
        self.client = client

    def get_substorage(self, relative_path):
        raise self.__class__(self.client.get_substorage(relative_path))
    
    def as_readonly(self):
        return ReadOnlyClient(self.client)

    def as_writeonly(self):
        return WriteOnlyClient(self.client)

    def get_bytes(self, key):
        return self.client.get_bytes(key)

    def put_bytes(self, key, value: bytes):
        return self.client.put_bytes(key, value)

    def put_bytes_stream(self, stream: Iterable[Tuple[str, bytes]]):
        return self.client.put_bytes_stream(stream)

class ReadOnlyClient(WrapperClient):
    def put_bytes(self, key, value: bytes):
        raise NotImplementedError()
    
    def put_bytes_stream(self, stream: Iterable[Tuple[str, bytes]]):
        raise NotImplementedError()

class WriteOnlyClient(WrapperClient):
    def get_bytes(self, key):
        raise NotImplementedError()


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


class LocalStorageClient(KeyValueClient):
    def __init__(self, root: str = "."):
        import os
        self.root = os.path.abspath(root)
        
    def get_substorage(self, relative_path):
        import os
        return self.__class__(os.path.join(self.root, relative_path))

    def put_bytes(self, key, value: bytes):
        import os
        filepath = os.path.join(self.root, key)
        parent_dir = os.path.dirname(filepath)
        if not os.path.exists(self.root):
            os.makedirs(self.root, exist_ok=True)
            
        with open(filepath, "wb") as f:
            f.write(value)
            
    def get_bytes(self, key) -> bytes:
        import os
        filepath = os.path.join(self.root, key)
        with open(filepath, "rb") as f:
            return f.read()
        
