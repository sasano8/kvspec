import os, shutil

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

    def ls(self, key: str = ""):
        import time

        path = self.get_path(key)

        # TODO: カレントディレクトリで返す値は異なるのだろうか？
        for file_or_dir in os.listdir(path):
            _ = self.get_path(file_or_dir)
            if os.path.isfile(_):
                yield file_or_dir

    def exists(self, key) -> bool:
        filepath = self.get_path(key)
        return os.path.isfile(filepath)

    def delete(self, key) -> bool:
        path = self.get_path(key)
        if not os.path.exists(path):
            return False

        if os.path.isfile(path):
            os.remove(path)
            return True
        elif os.path.isdir(path):
            # ディレクトリが空でなければTrueを返すことにする
            result = bool(os.listdir(path))
            shutil.rmtree(path)
            return result
        else:
            raise Exception()
