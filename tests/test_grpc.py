from unittest.mock import Mock
from kvspec.factory import KeyValueStoreGrpcClient

import pytest


def test_mock():
    mock_backend = Mock()


def test_serialize():
    from kvspec._grpc import keyvalue_pb2_grpc as stub
    from kvspec._grpc import keyvalue_pb2 as schema

    obj = schema.PutBytesReply(key="test")
    # print(obj.key)
    # print(obj.SerializeToString())
    # print(schema.PutBytesReply.FromString(obj.SerializeToString()))

    # class StreamMessage:
    #     type: int = 1
    #     body: bytes = b""


def test_put_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.put_bytes("test_put_bytes", b"value") == "test_put_bytes"


def test_get_bytes(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.get_bytes("test_put_bytes") == b"value"


def test_put_bytes_stream(grpc_client: KeyValueStoreGrpcClient):
    assert (
        grpc_client.put_bytes_stream("test_put_bytes_stream", [b"abc", b"def"])
        == "test_put_bytes_stream"
    )


def test_get_bytes_stream(grpc_client: KeyValueStoreGrpcClient):
    result = b""
    for chunk in grpc_client.get_bytes_stream("test_put_bytes_stream"):
        result += chunk

    assert b"abcdef"


def test_exists(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.exists("nothing") == False
    assert grpc_client.exists("test_put_bytes") == True


def test_delete(grpc_client: KeyValueStoreGrpcClient):
    path = grpc_client.put_bytes("test_delete", b"")
    assert grpc_client.exists(path)
    assert grpc_client.delete(path)
    assert not grpc_client.exists(path)


def test_ls(grpc_client: KeyValueStoreGrpcClient):
    assert grpc_client.ls("") == ["test_put_bytes", "test_put_bytes_stream"]

    with pytest.raises(Exception):
        assert grpc_client.ls("test_put_bytes")
