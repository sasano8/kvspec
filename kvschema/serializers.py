import os


class GeoDFSerializer:
    @staticmethod
    def load(f, format: str = "", **kwargs):
        import geopandas as gpd

        if not isinstance(f, str):
            raise Exception()

        _, ext = os.path.splitext(f)  # 拡張しの1文字目はドット
        ext = format or ext[1:]

        funcs = {
            "parquet": GeoDFSerializer.from_parquet,
            "geojson": GeoDFSerializer.from_geojson,
        }

        loader = funcs.get(ext, gpd.read_file)
        return loader(f, **kwargs)

    @staticmethod
    def dump(f, obj, format: str = "", **kwargs):
        import geopandas as gpd

        if not isinstance(f, str):
            raise Exception()

        _, ext = os.path.splitext(f)  # 拡張しの1文字目はドット
        ext = format or ext[1:]

        funcs = {
            "parquet": GeoDFSerializer.to_parquet,
            "geojson": GeoDFSerializer.to_geojson,
        }

        if ext not in funcs:
            raise Exception()

        dumper = funcs.get(ext)
        return dumper(f, obj, **kwargs)

    @staticmethod
    def from_parquet(f):
        """
        pandasでgeometryを含むparquetを読み込むと、geometry列はwkb形式となる。
        """
        import geopandas as gpd

        return gpd.read_parquet(f)

    @staticmethod
    def to_parquet(f, obj):
        import geopandas as gpd

        if not isinstance(obj, gpd.GeoDataFrame):
            raise Exception()
        obj.to_parquet(f)

    @staticmethod
    def from_geojson(f):
        import geopandas as gpd

        return gpd.read_file(f, driver="GeoJSON")

    @staticmethod
    def from_csv(f):
        import pandas as pd

        return pd.read_csv(f)

    @staticmethod
    def to_csv(f, obj):
        raise Exception("ヘッダーなどの問題で運用が難しいので禁止")
        import pandas as pd

        return obj.to_csv(f, index=False)

    @staticmethod
    def to_jsonline(f, obj):
        import pandas as pd

        if not isinstance(obj, pd.DataFrame):
            raise Exception()

        return obj.to_json(f, orient="records", force_ascii=False, lines=True)

    @staticmethod
    def to_geojson(f, obj):
        import geopandas as gpd

        if not isinstance(obj, gpd.GeoDataFrame):
            raise Exception()

        obj.to_file(f, driver="GeoJSON")

    @staticmethod
    def from_cbor(f):
        raise NotImplementedError()

    @staticmethod
    def to_cbor(f, obj):
        raise NotImplementedError()

    @staticmethod
    def from_postgresql(f):
        raise NotImplementedError()

    @staticmethod
    def to_postgresql(f, obj):
        raise NotImplementedError()

        def extract():
            import geopandas
            from geodatasets import get_path

            path_to_data = get_path("nybb")
            gdf = geopandas.read_file(path_to_data)
            return gdf

        def transform(gdf):
            gdf = gdf.to_crs("EPSG:4326")
            return gdf

        def load(gdf):
            from sqlalchemy import create_engine

            engine = create_engine(
                "postgresql://postgres:postgres@localhost:5432/postgres"
            )
            gdf.to_postgis(
                "nybb", engine, if_exists="fail", chunksize=2000, schema="public"
            )
            # gdf.to_postgis("nybb", engine, if_exists="append", chunksize=2000, schema="public")

        gdf = extract()
        gdf = transform(gdf)
        load(gdf)

    @staticmethod
    def from_orc(f):
        raise NotImplementedError()

    @staticmethod
    def to_orc(f):
        raise NotImplementedError()

    @staticmethod
    def sample():
        import geopandas as gpd
        from shapely.geometry import Point, Polygon

        # サンプルデータの作成
        data = {
            "City": ["Tokyo", "New York", "London"],
            "Country": ["Japan", "USA", "UK"],
            "Latitude": [35.6895, 40.7128, 51.5074],
            "Longitude": [139.6917, -74.0060, -0.1278],
        }

        # GeoDataFrameの作成
        gdf = gpd.GeoDataFrame(data)

        # 中心点ジオメトリーの追加
        gdf["Center"] = gdf.apply(
            lambda row: Point(row["Longitude"], row["Latitude"]), axis=1
        )

        # 架空の境界ジオメトリーの追加（例：正方形の境界）
        gdf["Boundary"] = gdf.apply(
            lambda row: Polygon(
                [
                    (row["Longitude"] - 0.1, row["Latitude"] - 0.1),
                    (row["Longitude"] + 0.1, row["Latitude"] - 0.1),
                    (row["Longitude"] + 0.1, row["Latitude"] + 0.1),
                    (row["Longitude"] - 0.1, row["Latitude"] + 0.1),
                ]
            ),
            axis=1,
        )

        # 主ジオメトリーを指定
        return gdf.set_geometry("Boundary")
