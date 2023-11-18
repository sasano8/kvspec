class Registry(dict):
    def loader(self, cls):
        self["loaders"][cls.__name__] = cls
        return cls

    def dumper(self, cls):
        self["dumpers"][cls.__name__] = cls
        return cls


builtins = Registry(loaders={}, dumpers={})
