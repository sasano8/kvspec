import pytest


def test_timestamp():
    from datetime import datetime, timezone
    from kvschema.encoders import TimestampEncoder, IsoFormat, Timestamp

    BASE_FLOAT = datetime(1970, 1, 1, tzinfo=timezone.utc).timestamp()
    BASE_STR = "1970-01-01T00:00:00+00:00"
    BASE_DT = datetime(1970, 1, 1, tzinfo=timezone.utc)

    # IsoFormat
    assert IsoFormat.from_isoformat(BASE_STR) == BASE_STR
    assert IsoFormat.from_datetime(BASE_DT) == BASE_STR
    assert IsoFormat.to_datetime(BASE_STR) == BASE_DT
    assert IsoFormat.to_timestamp(BASE_STR) == BASE_FLOAT

    with pytest.raises(Exception, match="Must be aware datetime"):
        assert IsoFormat.from_isoformat("1970-01-01T00:00:00")

    # Timestamp
    assert Timestamp.from_isoformat(BASE_STR) == BASE_FLOAT
    assert Timestamp.from_datetime(BASE_DT) == BASE_FLOAT
    assert Timestamp.to_datetime(BASE_FLOAT) == BASE_DT
    assert Timestamp.to_isoformat(BASE_FLOAT) == BASE_STR

    with pytest.raises(Exception, match="Must be aware datetime"):
        assert Timestamp.from_isoformat("1970-01-01T00:00:00")

    with pytest.raises(Exception, match="Must be aware datetime"):
        assert Timestamp.from_datetime(datetime(1970, 1, 1))

    # encoder.from_xxx
    encoder = TimestampEncoder

    assert encoder.from_int(0.0) == BASE_FLOAT
    assert encoder.from_float(0.0) == BASE_FLOAT
    assert encoder.from_number(0) == BASE_FLOAT
    assert encoder.from_number(0.0) == BASE_FLOAT
    assert encoder.from_str(BASE_STR) == BASE_FLOAT
    assert (
        encoder.from_datetime(datetime(1970, 1, 1, tzinfo=timezone.utc)) == BASE_FLOAT
    )

    # encoder.to_xxx
    assert encoder.to_float(BASE_FLOAT) == BASE_FLOAT
    assert encoder.to_timestamp(BASE_FLOAT) == BASE_FLOAT
    assert encoder.to_isoformat(BASE_FLOAT) == BASE_STR
    assert encoder.to_datetime(BASE_FLOAT) == BASE_DT
    assert encoder.to_datetime(BASE_FLOAT).tzinfo == timezone.utc

    with pytest.raises(Exception, match="Must be aware datetime"):
        encoder.from_str("1970-01-01T00:00:00")

    with pytest.raises(Exception, match="Must be aware datetime"):
        encoder.from_datetime(datetime(1970, 1, 1))

    # encoder.encode
    assert encoder.encode(BASE_FLOAT) == BASE_FLOAT
    assert encoder.encode(int(BASE_FLOAT)) == BASE_FLOAT
    assert encoder.encode(BASE_STR) == BASE_FLOAT
    assert encoder.encode(BASE_DT) == BASE_FLOAT

    # encoder.decode
    assert encoder.decode("default", BASE_FLOAT) == BASE_FLOAT
    assert encoder.decode("float", BASE_FLOAT) == BASE_FLOAT
    assert encoder.decode("float", int(BASE_FLOAT)) == BASE_FLOAT
    assert encoder.decode("timestamp", BASE_FLOAT) == BASE_FLOAT
    assert encoder.decode("str", BASE_FLOAT) == BASE_STR
    assert encoder.decode("isoformat", BASE_FLOAT) == BASE_STR
    assert encoder.decode("datetime", BASE_FLOAT) == BASE_DT


def test_serializer():
    import geopandas as gpd
    from kvschema.serializers import GeoDFSerializer
    from shapely.geometry.base import BaseGeometry
    from shapely import wkt

    BASE_DIR = "test_storage/"

    df1 = GeoDFSerializer.sample()
    GeoDFSerializer.dump(BASE_DIR + "geo1.parquet", df1)
    df2 = GeoDFSerializer.load(BASE_DIR + "geo1.parquet")

    row1 = df1.iloc[0]
    row2 = df2.iloc[0]

    columns = {
        "City": str,
        "Country": str,
        "Latitude": float,
        "Longitude": float,
        "Center": BaseGeometry,
        "Boundary": BaseGeometry,
    }

    assert len(df1.columns) == len(columns)

    for col, typ in columns.items():
        assert df1[col].equals(df2[col])
        assert df1[col].dtype == df2[col].dtype
        assert isinstance(df1.iloc[0][col], typ)
        assert isinstance(df2.iloc[0][col], typ)

    assert df1.columns.equals(df2.columns), "Column names mismatch"
    assert df1.shape == df2.shape, "Rows and columns count mismatch"  # 行と列数の比較
    assert df1.geometry.equals(df2.geometry), "Geometry data mismatch"
    assert (df1.geometry == df2.geometry).all(), "Geometry data mismatch"
    assert df1.crs == df2.crs, "CRS mismatch"

    assert df1.geometry.name == "Boundary"
    assert df2.geometry.name == "Boundary"

    df3 = df2.set_geometry("Center")
    assert df3.geometry.name == "Center"

    GeoDFSerializer.dump(BASE_DIR + "geo2.parquet", df3)
    df4 = GeoDFSerializer.load(BASE_DIR + "geo2.parquet")

    assert df4.geometry.name == "Center"

    # 対応ドライバの確認
    if False:
        # 一般的な地理空間IOライブラリ
        import fiona

        print(fiona.supported_drivers)
        {
            "DXF": "rw",
            "CSV": "raw",
            "OpenFileGDB": "raw",
            "ESRIJSON": "r",
            "ESRI Shapefile": "raw",
            "FlatGeobuf": "raw",
            "GeoJSON": "raw",
            "GeoJSONSeq": "raw",
            "GPKG": "raw",
            "GML": "rw",
            "OGR_GMT": "rw",
            "GPX": "rw",
            "MapInfo File": "raw",
            "DGN": "raw",
            "S57": "r",
            "SQLite": "raw",
            "TopoJSON": "r",
        }

    if False:
        # fiona より、GeoPandas に特化し、最適化が図られたライブラリ
        import pyogrio

        pyogrio.list_drivers()

    print(df4.info())
    """
    #   Column     Non-Null Count  Dtype   
    ---  ------     --------------  -----   
    0   City       3 non-null      object  
    1   Country    3 non-null      object  
    2   Latitude   3 non-null      float64 
    3   Longitude  3 non-null      float64 
    4   Center     3 non-null      geometry
    5   Boundary   3 non-null      geometry
    """

    with pytest.raises(Exception):
        # GeoJSONは１つのジオメトリーのみ保持できる
        # 複数のジオメトリーを保持する場合は、wktを復元したり手動の対応が必要
        df4.to_file(BASE_DIR + "geo3.json", driver="GeoJSON")

    df4["Boundary"] = df4["Boundary"].to_wkt()
    df4.to_file(BASE_DIR + "geo3.json", driver="GeoJSON")

    if False:
        # wkt列をgeometryに復元
        df4["Boundary"] = gpd.GeoSeries.from_wkt(df4["Boundary"])
        print(df4.info())
        print(df4.head())

        print("================")
        # 列名が返る <class 'str'>
        for row in df4:
            print(type(row))
            print(row)

        print("================")
        # NamedTupleのようなものが返る <class 'pandas.core.series.Series'>
        for index, row in df4.iterrows():
            print(type(row))
            print(row)

        print("================")
        # <class 'pandas.core.frame.Pandas'>
        for row in df4.itertuples():
            print(type(row))
            print(row.City)
