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
        
        # TODO: channel はスレッドセーフだが、並列実行時に注意する。
        # これに対処するには以下の方法を取る
        # 1. 可能ならレスポンスに含めるのが最もシンプルでよい
        # 2. それぞれでチャネルを作成する
        # 3. ロックやセマフォ で排他制御する（ロックされるためパフォーマンスに影響する）
        # 4. request_id で識別する
        """
        def client_download():
            metadata = [('request-id', request_id)]
            stub.Download(key=key, metadata=metadata)
        
            trailing_metadata.get("request-id").get("file-hash")
        
        def server_download(self, request_iterator, context):
            request_id = context.invocation_metadata().get('request-id')
            metadata = [
                ('request-id', json.dumps({"file-hash": file_hash.hexdigest()}))
            ]
            context.set_trailing_metadata(metadata)
        """
        
        
        metadata = dict(self.channel.trailing_metadata())
        file_size = metadata.get("file-size", "")
        file_hash = metadata.get("file-hash", "")
