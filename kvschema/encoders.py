from datetime import datetime, timezone
from typing import List, Literal, Type, Union


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

        # TODO: 機能していない
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
    @staticmethod
    def from_str(obj: str):
        return IsoFormat(obj).to_timestamp()

    from_isoformat = from_str

    @staticmethod
    def from_number(obj: Union[int, float]):
        return Timestamp(obj)

    @staticmethod
    def from_int(obj: int):
        return Timestamp(obj)

    @staticmethod
    def from_float(obj: float):
        return Timestamp(obj)

    from_timestamp = from_float

    @staticmethod
    def from_datetime(obj: datetime):
        return Timestamp.from_datetime(obj)

    @staticmethod
    def to_int(obj: float):
        return int(obj)

    @staticmethod
    def to_float(obj: float):
        return Timestamp(obj)

    @staticmethod
    def to_timestamp(obj: float):
        return Timestamp(obj)

    @staticmethod
    def to_isoformat(obj: float):
        return Timestamp.to_isoformat(obj)

    to_str = to_isoformat

    @staticmethod
    def to_datetime(obj: float):
        return Timestamp.to_datetime(obj)


class GeometryEncoder(
    AbstractEncoder,
    core_type=str,
    accept_types=[str, bytes, dict, "geometry"],
):
    @staticmethod
    def from_str(obj: str):
        raise NotImplementedError()

    @staticmethod
    def from_bytes(obj):
        raise NotImplementedError()

    @staticmethod
    def from_dict(obj):
        raise NotImplementedError()

    @staticmethod
    def from_geometry(obj):
        raise NotImplementedError()

    @staticmethod
    def to_geometry(obj):
        raise NotImplementedError()

    @staticmethod
    def to_str(obj):
        raise NotImplementedError()

    @staticmethod
    def to_bytes(obj):
        raise NotImplementedError()

    @staticmethod
    def to_dict(obj):
        raise NotImplementedError()

    from_wkt = from_str
    from_wkb = from_bytes
    from_geojson = from_dict
    to_wkt = to_str
    to_wkb = to_bytes
    to_geojson = to_dict
