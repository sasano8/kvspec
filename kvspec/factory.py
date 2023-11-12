import logging

from .storage import KeyValueClient
from ._grpc import keyvalue_pb2_grpc as stub
from ._grpc import keyvalue_pb2 as schema
from .service import KeyValueStoreService


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


def get_grpc_server(client: KeyValueClient):
    import grpc
    
    class LoggingInterceptor(grpc.ServerInterceptor):
        def intercept_service(self, continuation, handler_call_details):
            data = {"method": handler_call_details.method}
            data.update(handler_call_details.invocation_metadata)
            logging.info(data)
            return continuation(handler_call_details)
        
    from concurrent import futures
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[LoggingInterceptor()])
    stub.add_KeyValueStoreServicer_to_server(KeyValueStoreService(client), server)
    return server
    
def get_grpc_core_client(channel):
    obj = stub.KeyValueStoreStub(channel)
    return obj, schema

def get_grpc_client(channel) -> KeyValueStoreGrpcClient:
    return KeyValueStoreGrpcClient(channel)
    
def get_fastapi_router(client: KeyValueClient):
    raise NotImplementedError()
