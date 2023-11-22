import pytest


def test_timestamp():
    from datetime import datetime, timezone
    from kvschema.transforms import TimestampEncoder

    BASE_FLOAT = datetime(1970, 1, 1, tzinfo=timezone.utc).timestamp()
    BASE_DT = datetime(1970, 1, 1, tzinfo=timezone.utc)

    encoder = TimestampEncoder()

    assert encoder.from_int(0.0) == BASE_FLOAT
    assert encoder.from_float(0.0) == BASE_FLOAT
    assert encoder.from_number(0) == BASE_FLOAT
    assert encoder.from_number(0.0) == BASE_FLOAT
    assert encoder.from_str("1970-01-01T00:00:00+00:00") == BASE_FLOAT
    assert (
        encoder.from_datetime(datetime(1970, 1, 1, tzinfo=timezone.utc)) == BASE_FLOAT
    )

    assert encoder.to_float(BASE_FLOAT) == BASE_FLOAT
    assert encoder.to_timestamp(BASE_FLOAT) == BASE_FLOAT
    assert encoder.to_isoformat(BASE_FLOAT) == "1970-01-01T00:00:00+00:00"
    assert encoder.to_datetime(BASE_FLOAT) == BASE_DT
    assert encoder.to_datetime(BASE_FLOAT).tzinfo == timezone.utc

    with pytest.raises(Exception, match="Must be aware datetime"):
        encoder.from_str("1970-01-01T00:00:00")

    with pytest.raises(Exception, match="Must be aware datetime"):
        encoder.from_datetime(datetime(1970, 1, 1))