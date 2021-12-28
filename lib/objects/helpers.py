def multi_assert(*args, types):
    try:
        for arg in args:
            assert(isinstance(arg, types))
    except Exception:
        raise ObjectException


class ObjectException(Exception):
    pass


class Object:
    def __init__(self):
        pass

    def verify(self):
        raise ObjectException

    def as_dict(self):
        return vars(self)
