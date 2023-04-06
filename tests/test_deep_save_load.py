from random import choice
from string import ascii_letters
import pytest

from frozenclass import DataController


class PublicClassA:
    third = '123'


class PublicClassB:
    first = 123
    second = PublicClassA()


def test_save_load_deep_with_globals_bases():
    ts_object = PublicClassB()

    controller = DataController("test_saves")

    save_name = controller.deep_freeze(ts_object)

    new_class = controller.load_save(save_name)

    assert new_class.first == 123 and new_class.second.third == '123'


def test_save_load_deep_with_locals_bases():
    class LocalClassA:
        third = '123'


    class LocalClassB:
        first = 123
        second = LocalClassA()


    ts_object = LocalClassB()

    controller = DataController("test_saves")

    save_name = controller.deep_freeze(ts_object)

    new_class = controller.load_save(save_name)

    assert new_class.first == 123 and new_class.second.third == '123'
