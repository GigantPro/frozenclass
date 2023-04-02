from typing import Any


def parse_name(class_: Any) -> str:
    return str(type(class_)).split(".")[-1].split("'")[0]
