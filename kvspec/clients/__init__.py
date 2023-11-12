from typing import Iterable

from kvspec._grpc import keyvalue_pb2_grpc as stub
from kvspec._grpc import keyvalue_pb2 as schema


class KeyValueStoreGrpcClient:
    def __init__(self, channel):
        self.channel = channel
        self.stub = stub.KeyValueStoreStub(channel)
        
    def get_stub(self):
        return self.stub

    @staticmethod
    def get_schema():
        return schema
        
    def put_bytes(self, key: str, value: bytes) -> str:
        res = self.stub.PutBytes(schema.PutBytesRequest(key=key, value=value))
        return res.key
    
    def put_bytes_stream(self, key: str, stream: Iterable[bytes]) -> str:
        res = self.stub.PutBytesStream(schema.FileChunk(chunk=chunk) for chunk in stream)
        return res.key
    
    def get_bytes(self, key: str):
        res = self.stub.GetBytes(schema.GetBytesRequest(key=key))
        return res.value
    
    def get_bytes_stream(self, key: str):
        it = self.stub.GetBytesStream(schema.GetBytesRequest(key=key))

        for res in it:
            yield res.chunk
            
        metadata = dict(self.channel.trailing_metadata())
        file_size = metadata.get("file-size", "")
        file_hash = metadata.get("file-hash", "")
