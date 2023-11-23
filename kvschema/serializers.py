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
    def to_geojson(f, obj):
        import geopandas as gpd

        if not isinstance(obj, gpd.GeoDataFrame):
            raise Exception()

        obj.to_file(f, driver="GeoJSON")
    
    @staticmethod
    def from_postgresql(f):
        raise NotImplementedError()

    @staticmethod
    def to_postgresql(f, obj):
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
