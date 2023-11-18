from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class OneTimeIterator:
    def __init__(self, raw):
        self.raw = raw
        self.opend = False

    def __iter__(self):
        if self.opend:
            raise Exception("Already opened")
        else:
            it = iter(self.raw)
            self.opend = True
            return it

    def update(self, it):
        if self.opend:
            raise Exception("Already opened")
        self.it = it
        return it


class DumperBase:
    content_type = "application/jsonlines"

    def __init__(self, it):
        self.it = OneTimeIterator(it)

    def dump_to(self, f):
        for data in self:
            f.write(data)

    def __iter__(self):
        raise NotImplementedError()


class DataReader:
    def read(self, file_path: str):
        raise NotImplementedError()


class DataWriter:
    def write(self, data, file_path: str):
        raise NotImplementedError()


T = TypeVar("T", bound=DataReader)
U = TypeVar("U", bound=DataWriter)


class MyDumper(Generic[T, U]):
    def __init__(self, reader: T, writer: U):
        self.reader = reader
        self.writer = writer

    def dump(self, input_path: str, output_path: str):
        data = self.reader.read(input_path)
        self.writer.write(data, output_path)
