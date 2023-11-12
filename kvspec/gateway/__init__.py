import logging

from kvspec.backends import KeyValueClient
from kvspec._grpc import keyvalue_pb2_grpc as stub
from kvspec._grpc import keyvalue_pb2 as schema


class KeyValueStoreService(stub.KeyValueStoreServicer):
    def __init__(self, store: KeyValueClient):
        self.store = store
    
    def PutBytes(self, request, context):
        self.store.put_bytes(request.key, request.value)
        return schema.PutBytesReply(key=request.key)

    def GetBytes(self, request, context):
        result = self.store.get_bytes(request.key)
        return schema.GetBytesReply(value=result)


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
    