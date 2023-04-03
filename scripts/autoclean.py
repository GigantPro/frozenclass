from os import system


def autoclean():
    system("rm -rf dist")
    system("rm -rf frozenclass.egg-info")
    system("rm -rf .pytest_cache")
    system("rm -rf saves")
    system("rm -rf */__pycache__")
    system('rm -rf test_saves')
