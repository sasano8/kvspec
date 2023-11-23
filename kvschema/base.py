from functools import wraps, partial


class ExtensionMethod:
    def __init__(self, attribute_name, func):
        self.func = func
        self.attribute_name = attribute_name

    def _get_method(self, instance):
        obj = getattr(instance, self.attribute_name)
        return partial(self.func, obj)

    def __get__(self, instance, owner):
        if instance is None:
            return self.func
        else:
            return self._get_method(instance)


def extensionmethod(attribute_name="root"):
    def decorator(func):
        return wraps(func)(ExtensionMethod(attribute_name, func))

    return decorator
