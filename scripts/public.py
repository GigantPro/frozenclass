from .build import build
from os import system


def public() -> None:
    build()
    system('twine upload dist/*')
    print('SUCCESS')
