from .backends import KeyValueClient
from ._grpc import keyvalue_pb2_grpc as stub
from ._grpc import keyvalue_pb2 as schema
from .clients import KeyValueStoreGrpcClient
from .servers import get_grpc_server

    
def get_grpc_core_client(channel):
    obj = stub.KeyValueStoreStub(channel)
    return obj, schema

def get_grpc_client(channel) -> KeyValueStoreGrpcClient:
    return KeyValueStoreGrpcClient(channel)
    
def get_fastapi_router(client: KeyValueClient):
    raise NotImplementedError()
