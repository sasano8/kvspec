from .storage import KeyValueClient
from ._grpc import keyvalue_pb2_grpc as stub
from ._grpc import keyvalue_pb2 as schema


class KeyValueStoreService(stub.KeyValueStoreServicer):
    def __init__(self, store: KeyValueClient):
        self.store = store
    
    def PutBytes(self, request, context):
        self.store.put_bytes(request.key, request.value)
        return schema.PutBytesReply(key=request.key)

    def GetBytes(self, request, context):
        result = self.store.get_bytes(request.key)
        return schema.GetBytesReply(value=result)
