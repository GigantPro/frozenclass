from os import system


def start_testing() -> None:
    system('python -m unittest discover --pattern=*_test.py')
