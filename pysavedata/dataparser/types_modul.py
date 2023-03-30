import inspect
from typing import Any, Callable
from copy import deepcopy

from ..exceptions import Novariable


class TypesModule:
    def get_value_by_type(value: Any, type_: str) -> Any:
        _standart_types = {
            'int': int,
            'float': float,
            'list': list,
            'tuple': tuple,
            'str': str,
        }
        if _standart_types.get(type_, False):
            return _standart_types[type_](value)

        for class_name, class_obj in globals().items():
            if class_name == type_:
                return class_obj(value)
        return value

    def get_type_by_name(type_name: str) -> Any | None:
        for class_name, class_obj in globals().items():
            if class_name == type_name:
                return class_obj
        return None

    def create_class_with_data(class_: Callable, vars: dict[str: Any]) -> Any:
        init_args = inspect.getfullargspec(class_.__init__)
        init_args.args.remove('self')

        _vars = deepcopy(vars)
        print(_vars)
        vars_to_init = {}
        for var in init_args.args:
            if var not in _vars:
                raise Novariable(var)
            vars_to_init[var] = _vars[var]
            _vars.pop(var)
        res_class = class_(**vars_to_init)

        for var in _vars:
            setattr(res_class, var, _vars[var])

        return res_class

    def generate_class_by_info(info: dict) -> Any:
        new_type = type(info['type']['saved_class'], (object,), info['var'])
        setattr(new_type, '__name__', info['SavedModel']['save_name'])
        return new_type
