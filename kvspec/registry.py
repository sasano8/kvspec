class Registry(dict):
    def __init__(self):
        super().__init__()
        self["loaders"] = {}
        self["dumpers"] = {}

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(f"{key} not found in the registry.")
        return super().__getitem__(key)

    def loader(self, cls):
        self["loaders"][cls.__name__] = cls
        return cls

    def dumper(self, cls):
        self["dumpers"][cls.__name__] = cls
        return cls

builtins = Registry(loaders={}, dumpers={})
