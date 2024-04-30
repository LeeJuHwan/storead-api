def utilclass(cls):
    """
    Make all methods of a class static methods.
    """
    for name, value in cls.__dict__.items():
        if callable(value):
            setattr(cls, name, staticmethod(value))
    return cls
