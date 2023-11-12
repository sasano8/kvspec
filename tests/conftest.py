import pytest

from kvspec import factory, storage


@pytest.fixture(scope="module")
def local_storage():
    import os
    
    TEST_STORAGE = "test_storage"
    
    if not os.path.exists(TEST_STORAGE):
        os.makedirs(TEST_STORAGE, exist_ok=True)
    
    yield storage.LocalStorageClient(TEST_STORAGE)
    

@pytest.fixture(scope="module")
def grpc_server(local_storage):
    server = factory.get_grpc_server(local_storage)
    port = server.add_insecure_port('[::]:0')  # auto assign port
    server.start()
    yield port
    server.stop(None)


@pytest.fixture(scope="module")
def grpc_channel(grpc_server):
    import grpc

    port = grpc_server
    with grpc.insecure_channel(f'127.0.0.1:{port}') as channel:
        yield channel
    

@pytest.fixture(scope="module")
def grpc_client(grpc_channel):
    yield factory.get_grpc_client(grpc_channel)
