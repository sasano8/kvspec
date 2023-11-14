

# Update protobuf

`keyvalue.proto` を更新した場合、次のコマンドでgrpcスタブを再生成します。

```
make generate-grpc
```

# test

```
pytest -svx
```

# serve

Http(asgi)サーバーを起動します。

```
```

GraphQLサーバーを起動します。

```
uvicorn kvspec.servers._graphql:app --reload
```

Grpcサーバーを起動します。

```
```
