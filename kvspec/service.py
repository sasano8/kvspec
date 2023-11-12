from .storage import KeyValueClient
from ._grpc import keyvalue_pb2_grpc as stub
from ._grpc import keyvalue_pb2 as schema


class KeyValueStoreService(stub.KeyValueStoreServicer):
    def __init__(self, store: KeyValueClient):
        self.store = store
    
    def WriteBytes(self, request, context):
        self.store.write_bytes(request.key, request.value)
        return schema.WriteBytesReply(key=request.key)

    def ReadBytes(self, request, context):
        result = self.store.read_bytes(request.key)
        return schema.ReadBytesReply(value=result)
