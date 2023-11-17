from typing import Union
from urllib.parse import SplitResult as ParsedUrl, urlsplit
import os

from kvspec.backends.local import LocalStorageClient


def csv_to_dict(resource: LocalStorageClient, header: bool = True):
    with resource.open("", mode="r") as f:
        import csv

        if not header:
            raise NotImplementedError()

        csv_reader = csv.DictReader(f)  # headerを読み飛ばす
        # csv_reader = csv.DictReader(f, fieldnames=[])  # headerは読み飛ばされない
        for row in csv_reader:
            yield row


def parse_file_url(url_or_spec: Union[ParsedUrl, str]):
    if isinstance(url_or_spec, str):
        parsed = urlsplit(url_or_spec)
    else:
        parsed = url_or_spec

    print(parsed)
    schema = parsed.scheme
    if schema == "absfile":
        abs_or_rel = "/"
    elif schema == "relfile":
        abs_or_rel = ""
    else:
        raise Exception(f"Invalid schema: Must be abs or relative: {schema}")

    hostname = parsed.hostname or ""
    path = parsed.path or ""

    # 絶対パスが混じると絶対パスで上書きされてしまう
    while hostname.startswith("/"):
        hostname = hostname[1:]

    while path.startswith("/"):
        path = path[1:]

    path = os.path.join(abs_or_rel, hostname, path)

    return path
