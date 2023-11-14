import logging
import grpc

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

    def Ls(self, request, context):
        result = self.store.ls(request.key)
        return schema.LsReply(keys=list(result))

    def Exists(self, request, context):
        result = self.store.exists(request.key)
        return schema.ExistsReply(result=result)

    def Delete(self, request, context):
        result = self.store.delete(request.key)
        return schema.ExistsReply(result=result)

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


class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        data = {"method": handler_call_details.method}
        data.update(handler_call_details.invocation_metadata)
        logging.info(data)
        return continuation(handler_call_details)


def get_grpc_server(client: KeyValueClient):
    from concurrent import futures

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=[LoggingInterceptor()]
    )
    stub.add_KeyValueStoreServicer_to_server(KeyValueStoreService(client), server)
    return server


class GrpcServer:
    def __init__(
        self,
        client_args: str = "{}",
        host: str = "[::]",
        port: int = 0,  # defult: auto assign port
        max_workers: int = 1,
        # handlers: Any | None = None,
        # interceptors: Any | None = None,
        # options: Any | None = None,
        # maximum_concurrent_rpcs: Any | None = None,
        # compression: Any | None = None,
        # xds: bool = False
    ):
        from concurrent import futures

        client = client_args

        if max_workers == 1:
            thread_pool = None
        else:
            thread_pool = futures.ThreadPoolExecutor(max_workers=max_workers)

        server = grpc.server(thread_pool, interceptors=[LoggingInterceptor()])

        self.thread_pool = thread_pool
        self.server = server
        self.client = client

        service = KeyValueStoreService(self.client)
        stub.add_KeyValueStoreServicer_to_server(service, self.server)

        port = server.add_insecure_port(host + ":" + str(port))
        self.port = port

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

    def wait(self):
        raise NotImplementedError()

    def __init__(self):
        self.thread_pool
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
