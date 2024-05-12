class BaseSelector:
    validator = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _response(self, validation):
        if not validation.is_valid:
            raise validation.error
        return validation.data
