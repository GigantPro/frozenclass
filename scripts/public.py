from os import system

from .build import build


def public() -> None:
    system('rm -rf dist')
    system('rm -rf pysavedata.egg-info')

    build()
    system('twine upload dist/*')

    print('SUCCESS')
