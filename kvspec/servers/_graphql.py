from email import header
import strawberry
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from strawberry.asgi import GraphQL
from strawberry.fastapi import GraphQLRouter, BaseContext
from typing import Generator, Union, AsyncGenerator

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
    def get_text(self, info: Info, *, key: str) -> str:
        value = info.context.client.get_text(key)
        return value

    @strawberry.field
    def get_text2(self, info: Info, *, key: str) -> Union[str, None]:
        value = info.context.client.get_text(key)
        return value

    @strawberry.field
    def transaction(self, info: Info) -> str:
        # graphql でヘッダーを使うことは難しい
        # なぜなら、クエリは複数届く可能性があり、ヘッダーが衝突してしまう
        transaction_id = "abcdef"
        info.context.headers["transaction_id"] = transaction_id
        return transaction_id


COUNT = 0


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count_up(self) -> AsyncGenerator[int, None]:
        """通常のgeneratorは使用できない？"""
        import time
        import asyncio

        global COUNT
        while True:
            COUNT += 1
            yield COUNT
            await asyncio.sleep(1)
            # time.sleep(1)


TEST_STORAGE = "test_storage"
client = LocalStorageClient(TEST_STORAGE)


def get_storage():
    yield client


def create_context_dependency():
    def dependency(client=Depends(get_storage)):
        return Context(client=client)

    return dependency


# (4) スキーマを定義する
schema = strawberry.Schema(query=Query, subscription=Subscription)

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

"""
subscription MySubscription {
  value: countUp
}
"""
