from typing import Any, Callable

from .data_controller import DataController
from .exceptions import NoSave


def AutoFreeze(saves_path: str = 'saves', mode: str = 'freeze') -> Callable:
    """Automatically saves changes to variables made to the class

    Args:
        saves_path (str, optional): Path to save folder. Defaults to 'saves'.
        mode (str, optional): Save mode (as in DataController): 'freeze' or 'deep_freeze'. Defaults to 'freeze'.
    """
    def wrapper_func(target_class: Any) -> Any:
        if '__name__' not in target_class.__dict__:
            raise AttributeError('Your class must contain a variable called __name__')

        setattr(target_class, '__controller', DataController(saves_path))
        setattr(target_class, '__is_init', False)

        setattr(target_class, '__staff_params', [
            '__controller',
            '__is_init',
            '__old_setattr',
            '__freeze_class',
            '__old_init',
        ])

        def __custom_setattr(self, __name: str, __value: Any) -> Any:
            res = self.__old_setattr(__name, __value)

            if self.__is_init and __name not in self.__staff_params:
                self.__controller.dalete_save(self.__name__)
                __freeze_class(self)
            return res

        def __freeze_class(self) -> None:
            {
                'freeze': self.__controller.freeze_class,
                'deep_freeze': self.__controller.deep_freeze,
            }[mode](self, self.__name__)

        def __custom_init(self, *args, **kwargs) -> None:
            self.__old_init(*args, **kwargs)

            name = self.__name__
            try:
                saved_vars = getattr(self, '__controller').load_saved_vars(name)
            except NoSave:
                self.__freeze_class()
            else:
                # print(saved_vars)
                for saved_var in saved_vars:
                    self.__setattr__(saved_var, saved_vars[saved_var])

            self.__is_init = True

        setattr(target_class, '__freeze_class', __freeze_class)

        setattr(target_class, '__old_setattr', target_class.__setattr__)
        setattr(target_class, '__setattr__', __custom_setattr)

        setattr(target_class, '__old_init', target_class.__init__)
        setattr(target_class, '__init__', __custom_init)

        return target_class
    return wrapper_func
