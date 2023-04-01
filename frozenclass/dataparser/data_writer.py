from typing import Any
from random import randint
from datetime import datetime

from ..functions import parse_name
from .const import VAR_TEMPLATE, GLOBAL_TEMPLATE


class DataWriter:
    def __init__(self, saves_path: str, save_name: str | None = None) -> None:
        self.save_name = save_name
        self.saves_path = saves_path
        
        self.class_vars = None
        self.class_ = None

    def freeze_class(self, class_) -> bool:
        self._check_save_name(class_)
        self.class_ = class_
        
        self.class_vars = class_.__dir__()
        self.parsed_attributes = self._parse_attributes()

        self.save_data = self._create_save_data()
        
        with open(self.save_name, 'w', encoding='utf-8') as file:
            file.write(self.save_data)
        return True

    def _check_save_name(self, class_) -> None:
        if self.save_name is None:
            self.save_name = f'{self.saves_path}/{parse_name(class_)}' \
                    f'_{str(datetime.now()).split()[0]}_{randint(10**10, 10**11)}.save'
        else:
            self.save_name = f'{self.saves_path}/{self.saves_path}' \
                    f'_{str(datetime.now()).split()[0]}_{randint(10**10, 10**11)}.save'

    def _parse_attributes(self) -> dict:
        res = {}
        for attribute_name in self.class_vars:
            attrib_value = getattr(self.class_, attribute_name)
            if callable(attrib_value):
                continue
            res[attribute_name] = {
                'var_name': attribute_name,
                'var_type': self._parse_class_by_type(attrib_value),
                'var_value': attrib_value
            }
        return res

    def _parse_class_by_type(self, target_: Any) -> str:  # fix me 1
        str_type = str(type(target_))
        return str_type.split('\'')[-2].split('.')[-1]

    def _create_save_data(self) -> str:
        res = GLOBAL_TEMPLATE.format(
            save_name=self.save_name.split('/')[-1].split('.')[0],
            saved_class=self._parse_class_by_type(self.class_)
        )
        for attrname in self.parsed_attributes:
            res += '\n'
            res += VAR_TEMPLATE.format(**self.parsed_attributes[attrname])
        return res
