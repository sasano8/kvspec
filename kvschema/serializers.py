class GeoParquetSerializer:
    @staticmethod
    def dump(f, obj):
        import geopandas as gpd

        if isinstance(obj, gpd.GeoDataFrame):
            obj.to_parquet(f)
            # obj.to_file(f, driver="GeoJSON")

    @staticmethod
    def load(f):
        import geopandas as gpd

        return gpd.read_parquet(f)

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
