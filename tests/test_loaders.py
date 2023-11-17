from kvspec.loaders import functions as func


def test_parse_url():
    # schema に _ を含むことはできない
    assert func.parse_file_url("relfile://data/persons.csv") == "data/persons.csv"
    assert func.parse_file_url("relfile:///data/persons.csv") == "data/persons.csv"
    assert func.parse_file_url("absfile://data/persons.csv") == "/data/persons.csv"
    assert func.parse_file_url("absfile:///data/persons.csv") == "/data/persons.csv"


def test_loader():
    from kvspec.loaders.abstract import parse_and_get_dumper

    dumper = parse_and_get_dumper(
        registry=None,
        **{
            "url": "relfile://data/persons.csv",
            "loader": {"type": "csv_to_dict", "header": True},  # "csv", "json", "jsonl"
            "dumper": {"content-type": "application/jsonlines"},
        }
    )

    # FIXME: 空白が入ってしまう
    assert list(dumper) == ['{"id": "1", " name": " bob"}', "\n"]
