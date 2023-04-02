from os import system

from .build import build


def public() -> None:
    system("rm -rf dist")
    system("rm -rf frozenclass.egg-info")

    build()
    system("twine upload dist/*")

    system("rm -rf dist")
    system("rm -rf frozenclass.egg-info")

    print("SUCCESS")
