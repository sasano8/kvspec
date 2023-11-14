import strawberry
from fastapi import FastAPI, Depends
from strawberry.asgi import GraphQL
from strawberry.fastapi import GraphQLRouter, BaseContext
from typing import Union

from kvspec.backends import LocalStorageClient



# (2) User型を定義する
class Context(BaseContext):
    client: LocalStorageClient

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            
class Info:
    context: Context

@strawberry.type
class KeyValue:
    key: str
    value: str

# (3) Query(データの読み込み)を行うクラスを定義する
@strawberry.type
class Query:
    def __init__(self, client=None):
        self.client = client

    @strawberry.field
    def get_text(self, info: Info, *, key: str) -> KeyValue:
        value = info.context.client.get_text(key)
        return KeyValue(key=key, value=value)

    @strawberry.field
    def get_text2(self, info: Info, *, key: str) -> Union[str, None]:
        value = info.context.client.get_text(key)
        return value


TEST_STORAGE = "test_storage"
client = LocalStorageClient(TEST_STORAGE)


class QueueClient:
    def __init__(self):
        from collections import deque
        self.queue = deque(["1", "2", "3", "4"])
    
    def get_text(self, key):
        try:
            return self.queue.popleft()
        except IndexError:
            return None

client = QueueClient()

def get_storage():
    yield client

def create_context_dependency():
    def dependency(client = Depends(get_storage)):
        return Context(client=client)
    return dependency



# (4) スキーマを定義する
schema = strawberry.Schema(query=Query)

# (5) GraphQLエンドポイントを作成する
graphql_app = GraphQLRouter(schema, context_getter=create_context_dependency())

# (6) FastAPIアプリのインスタンスを作る
app = FastAPI()

# (7) /graphqlでGraphQL APIへアクセスできるようにし、適切なレスポンスを出力
app.include_router(graphql_app, prefix="/graphql")


"""
query MyQuery {
    # オブジェクト型
    getText(key: "test_put_bytes"){
        key
        value
    }
  
    # スカラー型
    getText2(key: "test_put_bytes")
    getText2(key: "test_put_bytes")
    third: getText2(key: "test_put_bytes")
}
"""
