from typing import Literal

def get_backend(backend_name: str, **kwargs):
    raise NotImplementedError()

def get_gateway(gateway_name: Literal["asgi", "grpc"], backend_name: str, **kwargs):
    backend = get_backend(backend_name, **kwargs)
    raise NotImplementedError()

def get_client(gateway_name: Literal["asgi", "grpc"], **kwargs):
    raise NotImplementedError()

def get_async_client(gateway_name: Literal["asgi", "grpc"], **kwargs):
    raise NotImplementedError()
