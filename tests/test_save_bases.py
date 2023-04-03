from random import choice
from string import ascii_letters
import pytest

from frozenclass import DataController


class PublicClassParent:
    fst = 123


class PublicClassChild(PublicClassParent):
    def __init__(self, thrd) -> None:
        self.thrd = thrd


@pytest.mark.parametrize(
    "thrd",
    [
        (1,),
        (2,),
        (2000000,),
        ("qwe",),
        ([1, 2, 3],),
        ({'1': 2},)
    ],
)
def test_save_load_with_globals_bases(thrd):
    save_name = ''.join([choice(ascii_letters) for _ in range(10)])

    ts_object = PublicClassChild(thrd)

    controller = DataController("test_saves")

    controller.freeze_class(ts_object, save_name)

    new_class = controller.load_save(save_name)

    assert new_class.thrd == thrd


@pytest.mark.parametrize(
    "thrd",
    [
        (1,),
        (2,),
        (2000000,),
        ("qwe",),
        ([1, 2, 3],),
        ({'1': 2},)
    ],
)
def test_save_load_with_globals_bases(thrd):
    class LocalClassParent:
        fst = 123


    class LocalClassChild(LocalClassParent):
        def __init__(self, thrd) -> None:
            self.thrd = thrd


    save_name = ''.join([choice(ascii_letters) for _ in range(10)])

    ts_object = LocalClassChild(thrd)

    controller = DataController("test_saves")

    controller.freeze_class(ts_object, save_name)

    new_class = controller.load_save(save_name)

    assert new_class.thrd == thrd