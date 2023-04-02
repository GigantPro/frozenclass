from typing import Any


class NoSave(Exception):
    def __init__(
        self, var_need: Any, message="There is no save with that name: {name}"
    ):
        self.var_need = var_need
        self.message = message
        super().__init__(self.message.format(name=var_need))
