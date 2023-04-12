from frozenclass import AutoFreeze, DataController


@AutoFreeze('test_saves')
class PublicClass:
    __name__ = 'Test with public'
    fst = 123
    sec = '123123'


def test_autosave_secorator_with_public_class():
    test_object = PublicClass()
    test_object.fst = 10

    controller = DataController('test_saves')
    loaded_class = controller.load_save('Test with public')

    assert test_object.fst == loaded_class.fst and test_object.sec == loaded_class.sec


def test_autosave_secorator_with_local_class():
    @AutoFreeze('test_saves')
    class LocalClass:
        __name__ = 'Test with local'
        fst = 123
        sec = '123123'


    test_object = LocalClass()
    test_object.fst = 10

    controller = DataController('test_saves')
    loaded_class = controller.load_save('Test with local')

    assert test_object.fst == loaded_class.fst and test_object.sec == loaded_class.sec
