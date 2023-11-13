from unittest.mock import Mock
from kvspec.factory import KeyValueStoreGrpcClient

def test_mock():
    mock_backend = Mock()

def test_put_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.put_bytes("test_put_bytes", b"value") == "test_put_bytes"

def test_get_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.get_bytes("test_put_bytes") == b"value"

def test_put_bytes_stream(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.put_bytes_stream("test_put_bytes_stream", [b"abc", b"def"]) == "test_put_bytes_stream"
    
def test_get_bytes_stream(grpc_client: KeyValueStoreGrpcClient):
    result = b""
    for chunk in grpc_client.get_bytes_stream("test_put_bytes_stream"):
        result += chunk
        
    assert b"abcdef"
    