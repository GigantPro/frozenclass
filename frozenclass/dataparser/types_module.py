import inspect
import json
from typing import Any, Callable, Union, Dict, Tuple

from ..exceptions import NoVar
from .const import STANDART_TYPES


def get_value_by_type(value: Any, type_: str) -> Any:
    if STANDART_TYPES.get(type_, False):
        return STANDART_TYPES[type_](value)

    for class_name, class_obj in globals().items():
        if class_name == type_:
            return class_obj(value)
    return value

def get_type_by_saved_type(type_data: str) -> Union[Any, None]:
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
    class_: Callable, vars: Dict[str, Any]
) -> Any:
    def _get_var_with_type(var_description: dict) -> Tuple[str, Any]:
        type_ = get_type_by_saved_type(var_description["class_path"])
        value = type_(var_description["var_value"])

        return var_description["var_name"], value

    if hasattr(class_, "__init__"):
        init_args = inspect.getfullargspec(class_.__init__)
        init_args.args.remove("self")

        remade_vars = {}
        for var_object in vars:
            remade_vars[var_object['var_name']] = {}
            for var_name in var_object:
                if var_name != 'var_name':
                    remade_vars[var_object['var_name']][var_name] = var_object[var_name]

        vars_to_init = {}
        for var in init_args.args:
            if var not in remade_vars:
                raise NoVar(var)
            vars_to_init[var] = get_value_by_type(
                remade_vars[var]['var_value'],
                remade_vars[var]['var_type'],
            )
        res_class = class_(**vars_to_init)

    else:
        res_class = class_()

    for var in vars:
        var_type_now = get_type_by_saved_type(var['class_path'])

        if var_type_now is None and var['class_path'] != 'NoneType' and not isinstance(var['var_value'], str):
            setattr(res_class, var['var_name'], var['var_value'])

        elif isinstance(var['var_value'], var_type_now):
            setattr(res_class, var['var_name'], var['var_value'])

        else:
            setattr(res_class, *_get_var_with_type(var))

    return res_class

def generate_class_by_info(info: dict) -> Any:
    parents = get_parents_by_json(info)

    new_type = type(info["type"]["saved_class"], parents, {})
    if not getattr(new_type, "__name__", False):
        setattr(new_type, "__name__", info["SavedModel"]["save_name"])
    return new_type

def get_json_bases_data_by_class(class_: Callable) -> str:
    s_bases = str(class_.__class__.__bases__)

    bases_list = s_bases.split('\'')[1::2]
    return json.dumps(bases_list)

def get_parents_by_json(json_: list) -> Tuple[Callable]:
    parents_list_str = json.loads(json_['type']['class_parents'])
    parents_list = [get_type_by_saved_type(parent) for parent in parents_list_str]
    for i in range(len(parents_list)):
        if parents_list[i] is None:
            parents_list[i] = type(parents_list_str[i], (object,), {})
    return tuple(parents_list)
