from .registry import builtins

# 使用しないが、import しておかないとregistryに登録されない
from . import dumpers
from . import loaders
from .loaders._file import FileLoader


def parse_dict(
    conf: dict = {
        "url": "relfile://data/persons.csv",
        "loader": {"type": "csv_to_dict", "header": True},  # "csv", "json", "jsonl"
        "dumper": {"content-type": "application/jsonlines"},
    }
):
    dumper = _get_dumper(conf)
    return dumper


def _get_storage(conf: dict):
    dumper_conf = conf["url"]


def _get_dumper(conf: dict):
    dumper_conf = conf["dumper"]
    dumper_cls = builtins.dumper(dumper_conf["content-type"])
    loader = _get_loader(conf)
    return dumper_cls(loader.load())


def _get_loader(conf: dict):
    loader_conf = conf["loader"]
    loader_cls = builtins.loader(loader_conf["type"])
    return loader_cls(**loader_conf["params"])


def parse_and_get_dumper(
    registry, url, loader: dict = {}, select: dict = {}, dumper: dict = {}
):
    from urllib.parse import urlparse, urlsplit, SplitResult

    # 参考
    # https://yourname:token@github.com:5555/tanaka/repo.git;param1=value1#section

    # urlparse, urlsplit は同じように見えるが、params をパースするか違いがある
    # paramsは古い仕様で近年使われないので無視してよい(urlsplitを使う)
    parsed_url = urlsplit(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc  # yourname:token@github.com:5555
    hostname = parsed_url.hostname  # github.com
    port = parsed_url.port  # 5555
    username = parsed_url.username  # yourname
    password = parsed_url.password  # token
    path = parsed_url.path  # /path
    query = parsed_url.query
    # params = parsed_url.params  # ; に続くパラメータ param1=value1  一般的に使われない
    fragment = parsed_url.fragment  # # に続くフラグメント section

    mapping = {
        "absfile": FileLoader,
        "relfile": FileLoader,
        "sftp": None,
        "s3": None,
        "http": None,
        "kafka": None,
        "postgresql": None,
    }

    cls = mapping.get(scheme, None)

    if not cls:
        raise Exception()

    loader = cls.load(
        registry=registry,
        url_or_spec=parsed_url,
        loader=loader,
        select=select,
        dumper=dumper,
    )

    return loader


# @dataclass
# class DataCatalog:
#     type: Literal[
#         "file", "sftp", "s3", "http", "kafka", "postgresql", "rest_postgresql"
#     ]
#     params: dict


{
    "url": "file://data.csv",
    "spec": {"type": "file", "path": "data.csv"},
    "loader": {"type": "csv_to_dict", "header": True},  # "csv", "json", "jsonl"
    "select": {"id": [], "created_at": ["str", "unixtime"], "geo": ["str", "geojson"]},
    "out": {
        "type": "object",
    },
}

{
    "url": "postgresql://public/mydata",
    "select": {
        "id": [],
        "created_at": ["timestamp", "unixtime"],
        "geo": ["geometry", "geojson"],
    },
    "out": {
        "object_type": "json",
        "content_type": "application/json"
        # "return_type": "application/octet-stream"
    },
}


class DataConverterFrom:
    """データを送信する際の変換方法を定義します"""

    @classmethod
    def parse(cls, src):
        ...

    def __init__(self, src):
        self.src = src

    def subscribe(self, data):
        ...


class DataConverterTo:
    """データを取得する際の変換方法を定義します"""

    @classmethod
    def parse(cls, dest):
        ...

    def __init__(self, dest):
        self.dest = dest

    def publish(self, data):
        ...


class DataConverterBus(DataConverterFrom, DataConverterTo):
    """データの送受信時の変換方法を定義します"""

    @classmethod
    def parse(cls, src, dest):
        ...

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

        self.src_converter = self.parse(src)
        self.dest_converter = self.parse(dest)

    def subscribe(self):
        ...

    def publish(self):
        ...

    def run(self):
        for data in self.subscribe():
            self.publish(data)
