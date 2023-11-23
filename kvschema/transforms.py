from datetime import datetime, timezone
from typing import List, Literal, Type, Union


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


class AbstractEncoder:
    def __init_subclass__(cls, core_type, accept_types: List[Union[str, Type]]) -> None:
        def map_str(cls, prefix, t):
            if isinstance(t, str):
                name = t.lower()
            elif isinstance(t, Type):
                name = t.__name__.lower()
            else:
                raise Exception(t)

            return name, getattr(cls, f"{prefix}{name}")

        def get_mapper(cls, prefix: Literal["from_", "to_"], *types):
            it = iter(types)

            name, func = map_str(cls, prefix, next(it))

            if prefix != "from_":
                yield "default", func
            yield name, func

            for typ in it:
                name, func = map_str(cls, prefix, typ)
                yield name, func

        def assert_not_duplicated(data: dict):
            keys = set()

            for k, v in data.items():
                if k in keys:
                    raise Exception(k)
                else:
                    keys.add(k)

        cls.core_type = core_type
        cls.encoders = dict(get_mapper(cls, "from_", core_type, *accept_types))
        cls.decoders = dict(get_mapper(cls, "to_", core_type, *accept_types))

        assert_not_duplicated(cls.encoders)
        assert_not_duplicated(cls.decoders)

    @classmethod
    def inspect_cls(cls):
        return {
            "core_type": cls.core_type.__name__.lower(),
            "encoders": list(cls.encoders.keys()),
            "decodres": list(cls.decoders.keys()),
        }

    @classmethod
    def encode(cls, obj):
        if obj is None:
            return None

        if isinstance(obj, datetime):
            from_ = "datetime"
        elif isinstance(obj, str):
            from_ = "str"
        elif isinstance(obj, int):
            from_ = "int"
        elif isinstance(obj, float):
            from_ = "float"
        else:
            raise Exception()

        if func := cls.encoders.get(from_, None):
            return func(obj)
        else:
            raise Exception((from_, cls.encoders))

    @classmethod
    def decode(cls, to: str, obj):
        if obj is None:
            return None

        if isinstance(obj, float):
            ...
        elif isinstance(obj, int):
            obj = float(obj)
        else:
            raise Exception(obj)

        if func := cls.decoders.get(to, None):
            return func(obj)
        else:
            raise Exception((to, cls.decoders))


class TimestampEncoder(
    AbstractEncoder,
    core_type=float,
    accept_types=[int, float, str, datetime, Timestamp, IsoFormat],
):
    @classmethod
    def from_str(cls, obj: str):
        return IsoFormat(obj).to_timestamp()

    from_isoformat = from_str

    @classmethod
    def from_number(cls, obj: Union[int, float]):
        return Timestamp(obj)

    @classmethod
    def from_int(cls, obj: int):
        return Timestamp(obj)

    @classmethod
    def from_float(cls, obj: float):
        return Timestamp(obj)

    from_timestamp = from_float

    @classmethod
    def from_datetime(cls, obj: datetime):
        return Timestamp.from_datetime(obj)

    @classmethod
    def to_int(cls, obj: float):
        return int(obj)

    @classmethod
    def to_float(cls, obj: float):
        return Timestamp(obj)

    @classmethod
    def to_timestamp(cls, obj: float):
        return Timestamp(obj)

    @classmethod
    def to_isoformat(cls, obj: float):
        return Timestamp.to_isoformat(obj)

    to_str = to_isoformat

    @classmethod
    def to_datetime(cls, obj: float):
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
