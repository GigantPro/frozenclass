from random import choice
from string import ascii_letters
import pytest

from frozenclass import DataController


@pytest.mark.parametrize(
    "fst, sec, thrd",
    [
        (1, 2, 3),
        (2, 3, 4),
        (10000000, 2000000, 23423456876),
        ("asd", "qwe", "zxcasd"),
        ([1, 2, 3], ['1', '2', '3'], (3, 4, 5)),
        ([1, '2', ['3', '4']], 1, 2),
        ({1: 2}, 2, '3'),
        ({2: ['1234']}, {3: 'asdqwe'}, ['123234']),
        ({2: ['1234']}, {3: 'asdqwe'}, ['123234']),
    ],
)
def test_save_load(fst, sec, thrd):
    class Test:
        pass

    save_name = ''.join([choice(ascii_letters) for _ in range(10)])

    ts_object = Test()

    setattr(ts_object, "fst", fst)
    setattr(ts_object, "sec", sec)
    setattr(ts_object, "thrd", thrd)

    controller = DataController("test_saves")

    controller.freeze_class(ts_object, save_name)

    new_class = controller.load_save(save_name)

    assert new_class.fst == fst and new_class.sec == sec and new_class.thrd == thrd
