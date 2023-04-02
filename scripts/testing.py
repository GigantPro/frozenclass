from os import system
import sys


def start_testing():
    system('pytest')

    platform = sys.platform
    if platform == 'win32':
        system('rmdir /a test_saves')
    else:
        system('rm -rf test_saves')
