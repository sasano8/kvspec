import logging

from kvspec.backends import KeyValueClient
from kvspec._grpc import keyvalue_pb2_grpc as stub
from kvspec._grpc import keyvalue_pb2 as schema


def send_hash_in_trailer(context, file_hash: str = ""):
    """
    ストリーミングでファイルを送信する場合、trailing_metadata（事後対応）でファイルのハッシュ値を送信可能。
    これにより、クライアントはファイルを正常に受け取れたか検証できる。
    """
    metadata = [("file-hash", file_hash)]
    context.set_trailing_metadata(metadata)

class KeyValueStoreService(stub.KeyValueStoreServicer):
    def __init__(self, store: KeyValueClient):
        self.store = store
    
    def PutBytes(self, request, context):
        self.store.put_bytes(request.key, request.value)
        return schema.PutBytesReply(key=request.key)

    def GetBytes(self, request, context):
        value = self.store.get_bytes(request.key)
        return schema.GetBytesReply(value=value)

    def PutBytesStream(self, request, context):
        it = iter(request)
        first = next(it)
        key: str = first.key
        value: bytes = first.chunk
        for req in it:
            value += req.chunk
        
        # context.invocation_metadata().get('request-id')
        self.store.put_bytes(key, value)  # ストリームに対応させる
        # self.store.put_bytes_stream(stream)  # TODO: 現在の実装はちょっと意味が違う
        return schema.PutBytesReply(key=key)

    def GetBytesStream(self, request, context):
        value = self.store.get_bytes(request.key)
        yield schema.FileChunk(chunk=value)


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
    