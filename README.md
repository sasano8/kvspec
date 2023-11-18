

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

    subgraph "DataBridge"
        I[Reader]
        K[Converter]
        J[Writer]
    end

    subgraph "Infrastructure"
        F[FileSystem]
        G[ObjectStorage]
        H[DatabaseTable]
        L[EventStream]
    end

    Http <-->|Request/Response| Application
    Application <-->|Read/Write| DataBridge
    DataBridge <-->|Read/Write| Infrastructure
```

## データフォーマット

データの取り扱いで問題となることが多いのは、日付とジオメトリーである。
調査した結果、GeoParquet が最も有望であると感じた。

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
        - Msgpack: JSONのバイナリ表現のようなフォーマットでJSONより高速です。ジオメトリーは直接サポートされていませんが、拡張型を使用することでサポートすることができます。
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
