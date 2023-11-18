import pandas as pd
import pyarrow as pa

from .abstract import DumperBase
from kvspec.registry import builtins


@builtins.dumper
class ParquetDumper(DumperBase):
    content_type = "application/parquet"

    def dump(self, filepath):
        df = pd.DataFrame(self.it)
        table = pa.Table.from_pandas(df)
        with pa.OSFile(filepath, "wb") as sink:
            with pa.RecordBatchFileWriter(sink, table.schema) as writer:
                writer.write_table(table)

    def _get_df(self):
        if isinstance(self.it, pd.DataFrame):
            df = self.it
        else:
            df = pd.DataFrame(self.it)
        return df

    def __iter__(self):
        df = self._get_df()

        json_str = df.to_json(orient="records", lines=True)
        for line in json_str.splitlines():
            yield line
            yield "\n"

    def to_jsonline_str(self) -> str:
        df = self._get_df()

        # epoch は1970年1月1日 00:00 が 0 となるが、それ以前は負の値になる
        json_str = df.to_json(
            orient="records", lines=True, force_ascii=False, date_format="epoch"
        )
        return json_str
