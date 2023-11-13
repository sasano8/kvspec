import os

from .abstract import KeyValueClient


class LocalStorageClient(KeyValueClient):
    def __init__(self, root: str = "."):
        import os
        self.root = os.path.abspath(root)
        
    def get_substorage(self, relative_path):
        import os
        return self.__class__(os.path.join(self.root, relative_path))

    def get_path(self, key):
        return os.path.join(self.root, key)

    def put_bytes(self, key, value: bytes):
        if not key:
            raise Exception()
        
        import os
        filepath = self.get_path(key)
        parent_dir = os.path.dirname(filepath)
        if not os.path.exists(parent_dir):
            os.makedirs(self.root, exist_ok=True)
            
        with open(filepath, "wb") as f:
            f.write(value)
            
    def get_bytes(self, key) -> bytes:
        filepath = self.get_path(key)
        with open(filepath, "rb") as f:
            return f.read()
        
    def exists(self, key) -> bool:
        filepath = self.get_path(key)
        return os.path.isfile(filepath)
    