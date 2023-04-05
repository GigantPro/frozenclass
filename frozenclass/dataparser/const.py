GLOBAL_TEMPLATE = """[SavedModel]
save_name={save_name}

[type]
saved_class={saved_class}
class_path={class_path}
class_parents={class_parents}
"""

VAR_TEMPLATE = """[var]
var_name={var_name}
var_type={var_type}
class_path={var_type_import}
var_value={var_value}
"""

BANNED_VAR_NAMES = (
    '__dict__',
    '__class__',
    '__module__',
)

STANDART_TYPES = {
    "int": int,
    "float": float, 
    "list": list,
    "tuple": tuple,
    "str": str,
    "dict": dict,
    "object": object,
}

STANDART_TYPES_TUPLE = tuple(type_ for type_ in STANDART_TYPES.values())

JSON_FORMATS = {
    "list": list,
    "dict": dict,
    "tuple": tuple,
}

BAD_SAVE_PHRASES = (
    'built-in method',
    'method-wrapper',
    'builtin_function_or_method',
)
