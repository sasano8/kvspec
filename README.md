

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

# kvspec

`kvspec`は、キーバリューストア（KVS）の抽象化を提供するPythonパッケージです。データの読み込みと書き込みを一元化し、様々なデータ形式とストレージタイプに対応します。

## 主な機能

- **KVSの抽象化**: `kvspec`は、データの読み込みと書き込みを一元化し、様々なKVSに対応します。データの読み込み元と書き込み先はURLで指定します。
- **データ形式のサポート**: CSV, JSON, JSONLなどの形式のデータを読み込み、JSONL形式で書き込む機能を提供します。
- **拡張性**: データ読み込みと書き込みの機能は、`Registry`クラスを通じて拡張することができます。新しいデータ形式やストレージタイプをサポートするために、独自のローダーとダンパーを追加することができます。

## 使用方法

```python
from kvspec import parse_dict

# データの読み込みと書き込みの設定
conf = {
    "url": "relfile://data/persons.csv",
    "loader": {"type": "csv_to_dict", "header": True},
    "dumper": {"content-type": "application/jsonlines"},
}

# データの読み込みと書き込みを実行
parse_dict(conf)
```

このコードは、`persons.csv`というCSVファイルからデータを読み込み、それをJSONL形式で書き込みます。

## インストール

`kvspec`パッケージは、Pythonのパッケージ管理ツールであるpipを使用してインストールできます：

```
pip install kvspec
```

## ライセンス

`kvspec`はMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。


## アーキテクチャ

``` mermaid
graph TD
    subgraph Http
        A[Grpc]
        B[OpenAPI]
        C[WebSocket]
        D[GraphQL]
    end

    subgraph Application
        X[Kvspec]
    end

    subgraph "Transform"
    end

    subgraph "Serialize"
    end

    subgraph "IOBridge"
        I[Reader]
        K[Converter]
        J[Writer]
    end

    subgraph "Infrastructure"
        F[FileSystem]
        G[ObjectStorage]
        H[DatabaseTable]
        L[EventStream]
        O[Http] <--> |Read/Write| Http
    end

    Http <-->|Request/Response| Application
    Application <-->|Read/Write| Transform
    Transform <-->|Read/Write| Serialize
    Serialize <-->|Read/Write| IOBridge
    IOBridge <-->|Read/Write| Infrastructure
```

- Transform: 日付やジオメトリー型をシリアライズ可能な型に変換する層
- Serialize: IOに対して読み書きする層
- Infrastructure: 永続化の具体的な実装層

## データフォーマット

データの取り扱いで問題となることが多いのは、ストリーム処理における日付とジオメトリーである。
調査した結果、GeoParquet が最も有望であると感じた。

- 一般的な
    - JSON: 広く知られたフォーマット
    - JsonLine: JSONの行単位のフォーマット。Json は大規模データの場合、メモリを圧迫するが行毎に読み込むことで、メモリを節約できる。
- 日付に関して
    - RFC3339(ISO 8601)形式のタイムスタンプを使用します。タイムスタンプの扱いに関して完全な標準は確立されておらず、IETF 標準化過程RFCでああるものの多くのプロジェクトで採用されています。
        - ISO 8601は多くの異なるフォーマットが許容されています
            - 1: 1999-12-31 23:59:59Z
            - 2: 1999-12-31 23:59:59+00
            - 3: 1999-12-31T23:59:59.999999Z
            - 4: 1999-12-31T23:59:59.999999+00:00
        - Zは「ゼロ時間オフセット」です
        - Pythonの `datetime.fromisoformat(dt)` でパース可能なのは 4 の形式のみです。
        - UTC 時間で管理するのが最も問題が生じません
        - フォーマットが統一されていればソート可能です
    - 日付型に関するフォーマット
        - Json: サポートしていない。一般的に、RFC3339の形式で文字列として表現する。シリアライズ時に、datetiem型を文字列として出力するが、デシリアライズ時は型情報が失われ、自動では日付型を復元できない。
        - Parquet: サポートしている。内部的には、1970年1月1日0時0分0秒(UTC)からの経過秒数で表現されるUNIX時間(エポック秒)で管理する。ミリ秒単位で記録され、符号付き64ビット整数（int64）で表現する。約292万年の範囲をカバー。
        - pickle: Pythonオブジェクトをシリアライズするためのフォーマット。制約なくシリアライズできる反面、動的にスクリプトが実行されるため、セキュリティ上の問題がある。
- ジオメトリーに関して
    - 問題点
        - データの大規模化: 理空間データの量が増加しており、これを効率的に処理、格納、分析することが課題となっている。
        - データ品質: 地理空間データはしばしば異なるソースから収集され、データの品質や形式の一貫性が不足している。
        - 互換性と標準化: 異なるGISソフトウェアやツール間でのデータの互換性が常に保証されるわけではなく、特定のフォーマットや標準が成熟していない。
    - 動向
        - クラウドベースのGIS: クラウドコンピューティングのため、クラウドネイティブなフォーマットの確立が進められている。
        - クラウドベースのGIS: クラウドコンピューティングの進展に伴い、地理空間データの分析、ストレージ、処理をクラウド上で行うソリューションが増加。スケーラビリティが向上している。
    - 組織
        - Open Geospatial Consortium (OGC): 地理空間情報の標準化を行う国際的な団体。GeoParquet を推進している。
        - International Organization for Standardization (ISO) - TC 211: 地理情報/地図製作に関する国際標準を策定している。
        - Federal Geographic Data Committee (FGDC): アメリカ合衆国で地理空間データの管理と使用に関する政策、調整、標準を提供する。
        - European Petroleum Survey Group (EPSG): 
    - ソフト・拡張機能
        - QGIS: 地理情報システム（GIS）のオープンソースソフトウェアです。
        - PostGIS: PostGISはPostgreSQLでジオメトリーを扱うための拡張機能です。GeoJSON, WKT, WKB などのフォーマットをサポートします。
        - GeoAlchemy: SQL Alchemyでジオメトリーを扱うための拡張機能です。
        - GEOPandas: Pandas でジオメトリーを扱うための拡張機能です。
    - フォーマット
        - GeoJSON: `{"type": "Feature", "geometry": {"type": "Point", "coordinates": [125.6, 10.1]}, "properties": {"name": "Dinagat Islands"}}`
        - WKT（Well-Known Text）: `POINT (30 10)\nLINESTRING (30 10, 10 30, 40 40)\nPOLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))`
        - WKB（Well-Known Binary）: WKT のバイナリ表現
        - BSON: MongoDBで採用されるJSONのバイナリ表現で、日付型や GeoJSON がサポートされています。
        - Shapefil: ジオメトリーを格納するためのファイルフォーマットですが、追加のメタデータを扱うには様々な制限があり、JSON などと比べて柔軟ではありません。
        - Msgpack: JSONのバイナリ表現のようなフォーマットでJSONより高速です。ジオメトリーは直接サポートされていませんが、拡張型を使用することでサポートすることができます。連続して書き込むことで、jsonline のようなフォーマットにすることも可能。
        - FlatGeobuf: GeoJSONをprotocol buffers でシリアライズしたフォーマット。
        - Parquet: 列指向フォーマットで圧縮性、高速性などJSONより分析に適しています。直接ジオメトリーをサポートしていませんが、メタデータなどを使用して拡張することができます。
        - GeoParquet: OGC が推進するジオメトリーをサポートするParquetの拡張フォーマット。
        - Geopackage: QGISで採用されるデフォルトのデータ形式
        - pickle: Pythonオブジェクトをシリアライズするためのフォーマット。制約なくシリアライズできる反面、動的にスクリプトが実行されるため、セキュリティ上の問題がある。

## Parquet について

- Parquetはバッチ処理向けに設計されており、ストリーミング処理に最適化されていません。小規模や頻繁な書き込み更新には向いていません。

## ユースケース

次のケースを考える。

- Parquet でデータを読み込む
- 日付型、ジオメトリー型を含むデータを Kafka で送信する。

Parquet は、日付型、ジオメトリー型をサポートしているが、ネットワークを経由して行を送信する際には、表現を変換する必要がある。
しかし、単一行で日付型、ジオメトリー型を扱うフォーマットが存在しない。

対応としては次のようなものが考えられる。

- スキーマ情報を管理し、シリアライズ・デシリアライズの方法を明示的に定める
- １行のParquet をデシリアライズ・シリアライズする（性能的には好ましくない）

## スキーマ

Confluent(kafka)でサポートされているスキーマは次の通り。

- Protocol Buffers: メタデータの取り扱いで難あり
- JSON Schema: Json の扱いで有効
- Avro: 最近はあまり使われないようだ

Json Schema では、メタデータ（仮に`transform`とした）を付与することができる。
これにより、文字列からジオメトリー型に復元するか判断を行うことができる。

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["created_at", "geom"],
  "properties": {
    "created_at": {
      "type": "float",
      "cast": "datetime"
      "description": "Unix timestamp",
    },
    "geom": {
      "type": "string",
      "cast": "geometry",
      "description": "Geometry"
    }
  }
}
```


## Geometry

``` geojson
{
  "type": "FeatureCollection",
  "features": [
    {
        "type": "Point", 
        "coordinates": [-115.1701692, 36.1224053],
        "properties": {
          "name": "Las Vegas"
        }
    },
    {
        "type": "Point", 
        "coordinates": [139.7725589, 35.6972466],
        "properties": {
          "name": "Tokyo"
        }
    },
    {
      "type": "Feature",
      "id": 1,
      "properties": {
        "ID": 0
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
              [-90,35],
              [-90,30],
              [-85,30],
              [-85,35],
              [-90,35]
          ]
        ]
      }
    }
  ]
}
```


# 参考

Kafka Connect

- AvroConverter
- ProtobufConverter
- JsonSchemaConverter
- JsonConverter
- StringConverter
- ByteArrayConverter

# fomart

{
  "envirnonment": {
    "dev": {
      "type": "docker-compose",
      "params": {
        "file": "docker-compose.override.dev.yml",
        "entrypoint": "python -m kvspec.servers._http",
        "args": [
          "--host",
          "0.0.0.0"
        ]
      }
    }
  },
  "connectors": {
    "db": "postgresql://admin:admin@localhost/admin"
  },
  "schema": {
    "world": {
      "type": "object",
      "required": ["created_at", "geom"],
      "properties": {
        "created_at": {
          "type": "float",
          "subtype": "datetime",
          "description": "Unix timestamp"
        },
        "geom": {
          "type": "string",
          "subtype": "geometry",
          "description": "Geometry"
        }
      }
    }
  },
  "srcs": {
    "mycsv": {
      "description": "",
      "path": "data/persons.csv",
      "type": "csv",
      "schema": "world"
    },
    "db": {
      "type": "postgres",
      "conenctor": "db",
      "schema": "public",
      "table": "users"
    }
  },
  "dests": {
    "alias": "myjsonl",
    "description": "",
    "path": "data/persons.jsonl",
    "type": "jsonl",
    "params": {
      "header": true
    }
  },
  "pipleline": [
    {
      "alias": "csv_to_jsonl",
      "loader": {
        "type": "GeoPandas",
        "srcs": ["mycsv"],
        "dests": ["stdout"]
      }
    }
  ]
}


# コマンドライン

pipleline:
	- alias: csv_to_jsonl
  	loader:
    	type: GeoPandas
    	src: mycsv
    	dest: myjsonl

```
cli src list
cli dest list
cli loader --type GeoPandas --schema world --src_path "data/persons.csv" --dest_path "data/persons.jsonl"
```

```
with Observable as thread:
  thread.from(KafkaTopic())
  .map(schema_validator)
  .subscribe(x => console.log(x));

  thread.from(KafkaTopic())
  .map(schema_validator)
  .subscribe(x => console.log(x));

  thread.wait()
```

streamzが参考になる

```
dest1 = KafkaTopic("topic1")
dest2 = KafkaTopic("topic2")
publish = Dispatcher(dest1, dest2)
balancer = LoadBalancer(dest1, dest2)

stream = Stream()

stream.map(lambda x: x + 1).sink(publish)

# dest1, dest2 にデータを送信します。
stream.emit(1)
gen.send(value)

for v in gen:
  gen.send(1)
```



```
{
  "type": "introspectionResponse",
  "resultCode": "A056001",
  "resultMessage": "[A056001] The access token is valid.",
  "action": "OK",
  "clientId": ...,
  "expiresAt": ...,
  "responseContent": "Bearer error=\"invalid_request\"",
  "scopes": [
    "payment": {
      "actions": ["create", "read", "update", "delete"]
    }
  ],
  "subject": "testuser01"
}
```

# cli

入力ソースを出力ソースに送信する。


```
python -m kvschema subscribe test_storage/inputs/persons.csv | python -m kvschema publish --dest stdout://
```


# objet mapping matrix

Pythonのメモリ空間にロードされたオブジェクトを標準出力やCSVに出力する場合、特殊なオブジェクトは次のように出力されます。
型情報が失われるため、元の型にオブジェクトを復元したい場合は、スキーマ情報が必要になります。

| 元の型 | 変換された型 | 表現 |
| ---- | ---- | ---- |
| datetime | string | isoformat |
| timestamp | string | isoformat |
| geometry | string | wkt |


## type safe format

型情報を含んだオブジェクトとしてのシリアライズ、型に適用したオブジェクトへのデシリアライズには次のファイル形式を利用してください。

| ファイル形式 | 備考 |
| ---- | ---- |
| parquet |  |
