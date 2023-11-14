from abc import ABC, abstractmethod
from typing import Iterable, Tuple

import uuid

class KeyValueClient(ABC):
    @abstractmethod
    def get_substorage(self, relative_path):
        raise NotImplementedError()
    
    def as_readonly(self):
        return ReadOnlyClient(self)

    def as_writeonly(self):
        return WriteOnlyClient(self)
    
    def ls(self, key: str = "", order_name="asc", order_updated="asc") -> Iterable[str]:
        raise NotImplementedError()

    def exists(self, key) -> bool:
        raise NotImplementedError()

    def delete(self, key) -> bool:
        raise NotImplementedError()

    def get_bytes(self, key) -> bytes:
        raise NotImplementedError()

    def put_bytes(self, key, value: bytes):
        raise NotImplementedError()
    
    def put_bytes_stream(self, stream: Iterable[Tuple[str, bytes]]):
        for key, value in stream:
            self.put_bytes(key, value)
            
    def get_text(self, key) -> str:
        return self.get_bytes(key).decode("utf-8")

    def put_text(self, key, value: str):
        return self.put_bytes(key, value.encode("utf-8"))
    
    def put_text_stream(self, stream: Iterable[Tuple[str, str]]):
        for key, value in stream:
            self.put_text(key, value)

    def touch(self, key: str = None) -> str:
        if key is None:
            for i in range(3):
                key = str(uuid.uuid4())
                if self.exists(key):
                    key = None
                    continue
                else:
                    break
            
            if not key:
                raise Exception("Failed generate uuid.")

        return self.put_bytes(key, b"")


class WrapperClient(KeyValueClient):
    def __init__(self, client: KeyValueClient):
        self.client = client

    def get_substorage(self, relative_path):
        raise self.__class__(self.client.get_substorage(relative_path))
    
    def as_readonly(self):
        return ReadOnlyClient(self.client)

    def as_writeonly(self):
        return WriteOnlyClient(self.client)
    
    def exists(self, key) -> bool:
        return self.client.exists(key)

    def get_bytes(self, key):
        return self.client.get_bytes(key)

    def put_bytes(self, key, value: bytes):
        return self.client.put_bytes(key, value)

    def put_bytes_stream(self, stream: Iterable[Tuple[str, bytes]]):
        return self.client.put_bytes_stream(stream)

class ReadOnlyClient(WrapperClient):
    def delete(self, key):
        raise NotImplementedError()
    
    def put_bytes(self, key, value: bytes):
        raise NotImplementedError()
    
    def put_bytes_stream(self, stream: Iterable[Tuple[str, bytes]]):
        raise NotImplementedError()

class WriteOnlyClient(WrapperClient):
    def exists(self, key) -> bool:
        raise NotImplementedError()

    def get_bytes(self, key):
        raise NotImplementedError()
