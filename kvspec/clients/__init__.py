from kvspec._grpc import keyvalue_pb2_grpc as stub
from kvspec._grpc import keyvalue_pb2 as schema


class KeyValueStoreGrpcClient:
    def __init__(self, channel):
        self.stub = stub.KeyValueStoreStub(channel)
        
    def get_stub(self):
        return self.stub

    @staticmethod
    def get_schema():
        return schema
        
    def put_bytes(self, key: str, value: bytes) -> str:
        response = self.stub.PutBytes(schema.PutBytesRequest(key=key, value=value))
        return response.key
    
    def get_bytes(self, key: str):
        response = self.stub.GetBytes(schema.GetBytesRequest(key=key))
        return response.value
