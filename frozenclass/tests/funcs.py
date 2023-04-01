import random
from string import ascii_letters

from ..functions import parse_name

__all__ = (
    'generate_test_file',
)


GLOBAL_TEMPLATE = '''
[SavedModel]
save_name={save_name}

[type]
saved_class={saved_class}
'''

VAR_TEMPLATE = '''
[var]
var_name={var_name}
var_type={var_type}
var_value={var_value}
'''


def generate_test_file() -> tuple[str, dict]:
    args = {
        'save_name': ''.join(random.choices(ascii_letters, k=random.randint(5, 15))),
        'saved_class': ''.join(random.choices(ascii_letters, k=random.randint(5, 15))),
        'vars': [generate_var() for _ in range(random.randint(1, 15))],
    }

    return GLOBAL_TEMPLATE.format(**args) + '\n'.join([i[0] for i in args['vars']]), args

def generate_var() -> tuple[str, dict]:
    kwargs = {
        'var_name': ''.join(random.choices(ascii_letters, k=random.randint(5, 15))),
        'var_type': ''.join(random.choices(ascii_letters, k=random.randint(5, 15))),
        'var_value': ''.join(random.choices(ascii_letters, k=random.randint(5, 15))),
    }

    return VAR_TEMPLATE.format(**kwargs), kwargs

def check_res(res: list, config: dict) -> bool:
    for class_ in res:
        if class_.__name__ != config['save_name']:
            return False

        if parse_name(class_) != config['saved_class']:
            return False

        for var in config['vars']:
            var_ = getattr(class_, var[-1]['var_name'])
            if var_ != var[-1]['var_value']:
                return False

    return True
