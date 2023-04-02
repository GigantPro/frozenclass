import pytest
from random import choice
from string import ascii_letters

from frozenclass import DataController


@pytest.mark.parametrize(
    "a, b, c",
    [
        (1, 2, 3),
        (2, 3, 4),
        (10000000, 2000000, 23423456876),
        ("asd", "qwe", "zxcasd"),
        ([1, 2, 3], ['1', '2', '3'], (3, 4, 5))
    ],
)
def test_save_load(a, b, c):
    class Test:
        pass
    
    save_name = ''.join([choice(ascii_letters) for _ in range(10)])

    ts_object = Test()

    setattr(ts_object, "a", a)
    setattr(ts_object, "b", b)
    setattr(ts_object, "c", c)

    controller = DataController("test_saves")

    controller.freeze_class(ts_object, save_name)

    new_class = controller.load_save(save_name)

    assert new_class.a == a and new_class.b == b and new_class.c == c

test_save_load([1, 2, 3], ['1', '2', '3'], (3, 4, 5))
