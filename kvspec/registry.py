class Registry(dict):
    def __init__(self):
        super().__init__()
        self["schemas"] = {}
        self["loaders"] = {}
        self["dumpers"] = {}

    def copy(self):
        import copy

        return copy.deepcopy(self)

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(f"{key} not found in the registry.")
        return super().__getitem__(key)

    def schemas(self, cls):
        if cls.__name__ in self["loaders"]:
            raise KeyError(f"{cls.__name__} is already registered.")

        self["loaders"][cls.__name__] = cls
        return cls

    def loader(self, cls):
        if cls.__name__ in self["loaders"]:
            raise KeyError(f"{cls.__name__} is already registered.")

        self["loaders"][cls.__name__] = cls
        return cls

    def dumper(self, cls):
        if cls.__name__ in self["loaders"]:
            raise KeyError(f"{cls.__name__} is already registered.")

        self["dumpers"][cls.__name__] = cls
        return cls


builtins = Registry()
