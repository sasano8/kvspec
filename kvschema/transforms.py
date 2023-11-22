from datetime import datetime, timezone
from typing import Union
from typing_extensions import Annotated


class UnixTime(float):
    ...


class Accepts:
    def __init__(self, *types):
        self.types = types


class IsoFormat(str):
    def to_timestamp(self) -> "Timestamp":
        dt = datetime.fromisoformat(self)
        if dt.tzinfo is None:
            raise Exception(f"Must be aware datetime: {self}")
        return Timestamp(dt.timestamp())

    def to_datetime(self):
        dt = datetime.fromisoformat(self)
        if dt.tzinfo is None:
            raise Exception(f"Must be aware datetime: {self}")
        return dt

    @classmethod
    def from_datetime(cls, obj: datetime):
        if obj.tzinfo is None:
            raise Exception(f"Must be aware datetime: {obj}")
        return cls(obj.isoformat())

    @classmethod
    def from_isoformat(cls, obj: str):
        dt = datetime.fromisoformat(obj)
        if dt.tzinfo is None:
            raise Exception(f"Must be aware datetime: {obj}")
        return cls(obj)


class Timestamp(float):
    def to_isoformat(self) -> IsoFormat:
        return IsoFormat(datetime.fromtimestamp(self, tz=timezone.utc).isoformat())

    def to_datetime(self):
        return datetime.fromtimestamp(self, tz=timezone.utc)

    @classmethod
    def from_datetime(cls, obj: datetime):
        if obj.tzinfo is None:
            raise Exception(f"Must be aware datetime: {obj}")
        return cls(obj.timestamp())

    @classmethod
    def from_isoformat(cls, obj: str):
        return IsoFormat.to_timestamp(obj)


class TimestampEncoder:
    raw: Annotated[
        float,
        Accepts(int, float, datetime, Timestamp, IsoFormat, datetime, "PdTimestamp"),
    ]

    def from_str(self, obj: str):
        return IsoFormat(obj).to_timestamp()

    def from_number(self, obj: Union[int, float]):
        return Timestamp(obj)

    def from_int(self, obj: int):
        return Timestamp(obj)

    def from_float(self, obj: float):
        return Timestamp(obj)

    def from_datetime(self, obj: datetime):
        return Timestamp.from_datetime(obj)

    def to_float(self, obj: float):
        return Timestamp(obj)

    def to_timestamp(self, obj: float):
        return Timestamp(obj)

    def to_isoformat(self, obj: float):
        return Timestamp.to_isoformat(obj)

    def to_datetime(self, obj: float):
        return Timestamp.to_datetime(obj)


def wkt_to_geometry(value: str = None):
    if value is None:
        return None

    raise Exception()


def geometry_to_wkt(value=None):
    if value is None:
        return None

    raise Exception()


def date_to_iso(value: datetime = None):
    if value is None:
        return None

    if not isinstance(value, datetime):
        raise Exception("Not datetime object.")

    offset = value.utcoffset()
    if offset is None:
        raise Exception("Naive datetime is not allowed.")
    elif not offset:
        # offset == 0 つまり UTC
        return value.isoformat()
    else:
        return value.astimezone(timezone.utc).isoformat()


def date_to_timestamp(value: datetime = None):
    if value is None:
        return None

    assert datetime(1, 1, 2).timestamp() == -62135543939.0
    assert datetime(1, 1, 1).timestamp()  # ValueError: year 0 is out of range

    raise Exception()


def iso_to_date(value: str = None):
    if value is None:
        return None

    raise Exception()
