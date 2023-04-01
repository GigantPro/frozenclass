from os import system


def start_linting():
    system("pylint -j$(nproc) $(git ls-files '*.py')")
