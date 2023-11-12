

# Update protobuf

`keyvalue.proto` を更新した場合、次のコマンドでgrpcスタブを再生成します。

```
make generate-grpc
```

# test

```
pytest -svx
```
