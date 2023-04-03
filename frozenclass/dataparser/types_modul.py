import inspect
import json
from typing import Any, Callable
from copy import deepcopy

from ..exceptions import NoVar
from .const import STANDART_TYPES


class TypesModule:
    def __init__(self) -> None:
        pass

    def get_value_by_type(self, value: Any, type_: str) -> Any:  # fix me 1
        if STANDART_TYPES.get(type_, False):
            return STANDART_TYPES[type_](value)

        for class_name, class_obj in globals().items():
            if class_name == type_:
                return class_obj(value)
        return value

    def get_type_by_saved_type(self, type_data: str) -> Any | None:
        components = type_data.split(".")
        if components[0] in STANDART_TYPES:
            return STANDART_TYPES[components[0]]

        mod = __import__(components[0])
        try:
            for comp in components[1:]:
                mod = getattr(mod, comp)
        except AttributeError:
            mod = None
        return mod

    def create_class_instance(
        self, class_: Callable, vars: dict[str:Any]
    ) -> Any:  # Fix me переделать под наследование
        def _get_var_with_type(var_description: dict) -> tuple[str, Any]:
            type_ = self.get_type_by_saved_type(var_description["class_path"])
            value = type_(var_description["var_value"])

            return var_description["var_name"], value

        print(vars)

        if hasattr(class_, "__init__"):
            init_args = inspect.getfullargspec(class_.__init__)
            init_args.args.remove("self")

            _vars = deepcopy(vars)
            vars_to_init = {}
            for var in init_args.args:
                if var not in _vars:
                    raise NoVar(var)
                vars_to_init[var] = _vars[var]
                _vars.pop(var)
            res_class = class_(**vars_to_init)

        else:
            res_class = class_()

        for var in vars:
            setattr(res_class, *_get_var_with_type(var))

        return res_class

    def generate_class_by_info(self, info: dict) -> Any:
        parents = self.get_parents_by_json(info)

        new_type = type(info["type"]["saved_class"], parents, {})
        if not getattr(new_type, "__name__", False):
            setattr(new_type, "__name__", info["SavedModel"]["save_name"])
        return new_type

    def get_json_bases_data_by_class(self, class_: Callable) -> str:
        s_bases = str(class_.__class__.__bases__)

        bases_list = s_bases.split('\'')[1::2]
        return json.dumps(bases_list)

    def get_parents_by_json(self, json_: list) -> tuple[Callable]:
        parents_list_str = json.loads(json_['type']['class_parents'])
        parents_list = [self.get_type_by_saved_type(parent) for parent in parents_list_str]
        for i in range(len(parents_list)):
            if parents_list[i] is None:
                parents_list[i] = type(parents_list_str[i], (object,), {})
        return tuple(parents_list)
