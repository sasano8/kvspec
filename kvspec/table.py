from uuid import uuid4
from contextlib import asynccontextmanager

Undefined = object()

class DictTable:
    selector = None
    publisher = None
    schema = None

    def __init__(self, store: dict = None):
        self.db = store or {}
        if not isinstance(self.db, dict):
            raise Exception()

    @classmethod
    def create_store(cls, store: dict, selector = None, publisher = None, schema = None):
        selector = selector or cls.selector
        publisher = publisher or cls.publisher
        schema = schema or cls.schema

        class TempStore(DictTable, selector=selector, publisher=publisher, schema=schema):
            ...
            
        return TempStore(store)
        
    def __str__(self):
        return self.db.__str__()
        
    def __repr__(self):
        return self.db.__repr__()
        
    def __init_subclass__(cls, selector, publisher, schema) -> None:
        cls.selector = staticmethod(selector)
        cls.publisher = staticmethod(publisher)
        cls.schema = staticmethod(publisher)

    async def insert(self, **obj):
        try:
            key = self.selector(obj)
            has_key = True
        except Exception:
            has_key = False

        if has_key:
            if key in self.db:
                raise KeyError("duplicate")
            self.db[key] = obj
            return obj
        else:    
            while True:
                self.publisher(obj)
                key = self.selector(obj)
                if key not in self.db:
                    break
            self.db[key] = obj
            return obj
        
    async def upsert(self, **obj):
        try:
            key = self.selector(obj)
        except Exception:
            self.publisher(obj)
            return self.upsert(**obj)

        self.db[key] = obj
        return obj

    async def get(self, key):
        return self.db[key]

    async def delete(self, key):
        res = self.db.pop(key, Undefined)
        if res is Undefined:
            return 0
        else:
            return 1

    async def keys(self):
        async for key in self.db.keys():
            yield key
        
    async def values(self):
        async for value in self.db.values():
            yield value

    async def items(self):
        async for key, value in self.db.items():
            yield key, value
    
    @asynccontextmanager
    async def transaction(self):
        yield self
        
    async def commit(self):
        ...


async def sample():
    def select_id(obj):
        return obj["id"]

    def publish_key_by_uuid4(obj):
        obj["id"] = str(uuid4())


    class SelectableStore2(
        DictTable,
        selector=select_id,
        publisher=publish_key_by_uuid4,
        schema=None
    ):
        ...

    store = SelectableStore2()
    
    async with store.transaction() as tr:
        await tr.insert()
        await tr.insert(id="1")
        await tr.insert(id="2")
        await tr.upsert()
        await tr.upsert(id="2")
        await tr.delete("3")
