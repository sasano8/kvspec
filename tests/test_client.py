from unittest.mock import Mock
from kvspec.factory import KeyValueStoreGrpcClient

def test_mock():
    mock_backend = Mock()

def test_write_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.write_bytes("sample", b"value") == "sample"

def test_read_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.read_bytes("sample") == b"value"
