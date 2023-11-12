from unittest.mock import Mock
from kvspec.factory import KeyValueStoreGrpcClient

def test_mock():
    mock_backend = Mock()

def test_put_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.put_bytes("sample", b"value") == "sample"

def test_get_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.get_bytes("sample") == b"value"
