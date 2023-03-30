__all__ = (
    'SavedModel',
)


class SavedModel:
    def __init__(self, *args, **kwargs) -> None:
        self.args, self.kwargs = args, kwargs