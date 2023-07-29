from copy import deepcopy
import json
from typing import Any, Callable, Optional, Tuple
from random import randint
from datetime import datetime

from .types_module import get_json_bases_data_by_class, get_type_by_saved_type
from .const import (
    BAD_SAVE_PHRASES,
    JSON_FORMATS,
    VAR_TEMPLATE,
    GLOBAL_TEMPLATE,
    BANNED_VAR_NAMES,
    STANDART_TYPES,
)


class DataWriter:
    def __init__(self, saves_path: str, save_name: Optional[str] = None) -> None:
        self.save_name = save_name
        self.saves_path = saves_path

        self.parsed_attributes = None
        self.saved_path = None
        self.class_vars = None
        self.save_data = None
        self.class_ = None

    def freeze_class(self, class_: Callable) -> str:
        self._check_save_name()
        self.class_ = class_

        self.class_vars = class_.__dir__()
        self.parsed_attributes = self._parse_attributes()
        self._vars_filter()
        self._remake_dict_keys()

        self.save_data = self._create_save_data()

        with open(self.saved_path, "w", encoding="utf-8") as file:
            file.write(self.save_data)
        return self.save_name

    def _check_save_name(self) -> None:
        if self.save_name is None:
            self.save_name = f'{"".join([str(randint(0, 10)) for _ in range(10)])}'

        self.saved_path = (
            f"{self.saves_path}/{self.save_name}_"
            f"{str(datetime.now()).split()[0]}_{randint(10**10, 10**11)}.save"
        )

    def _parse_attributes(self) -> dict:
        res = {}
        for attribute_name in self.class_vars:
            attrib_value = getattr(self.class_, attribute_name)
            if callable(attrib_value):
                continue
            res[attribute_name] = {
                "var_name": attribute_name,
                "var_type": self._parse_type_by_target(attrib_value)[0],
                "var_type_import": self._parse_type_by_target(attrib_value)[1],
                "var_value": attrib_value,
            }
        return res

    def _parse_type_by_target(self, target_: Any) -> Tuple[str]:
        str_type = str(type(target_))
        return str_type.split("'")[-2].split(".")[-1], str_type.split("'")[-2]

    def _create_save_data(self) -> str:
        res = GLOBAL_TEMPLATE.format(
            save_name=self.save_name,
            saved_class=self._parse_type_by_target(self.class_)[0],
            class_path=self._parse_type_by_target(self.class_)[1],
            class_parents=get_json_bases_data_by_class(self.class_),
        )
        for attrname in self.parsed_attributes:
            res += "\n"
            if self.parsed_attributes[attrname]['var_type'] in JSON_FORMATS:
                new_attr = deepcopy(self.parsed_attributes[attrname])
                new_attr['var_value'] = json.dumps(new_attr['var_value'])

                res += VAR_TEMPLATE.format(**new_attr)
            else:
                res += VAR_TEMPLATE.format(**self.parsed_attributes[attrname])
        return res

    def _vars_filter(self) -> None:
        new_attr = {}

        for banned_var in BANNED_VAR_NAMES:
            self.parsed_attributes.pop(banned_var, None)

        for var_name in self.parsed_attributes:
            if self.parsed_attributes[var_name]["var_type"] != "NoneType" and\
                self.parsed_attributes[var_name]["var_type"] in STANDART_TYPES:
                new_attr[var_name] = self.parsed_attributes[var_name]

        self.parsed_attributes = new_attr

    def _remake_dict_keys(self) -> None:
        for var_name in self.parsed_attributes:
            if self.parsed_attributes[var_name]['var_type'] == 'dict':
                self.parsed_attributes[var_name]['var_value'] = \
                    self.__add_marks_for_dict(self.parsed_attributes[var_name]['var_value'])

    def __add_marks_for_dict(self, dict_vals: dict) -> dict:
        new_dict = {}
        for key in dict_vals:
            if not isinstance(key, str):
                new_key = self.___processing_marks(key)
                new_dict[new_key] = dict_vals[key]
            else:
                new_dict[key] = dict_vals[key]
        return new_dict

    def ___processing_marks(self, value: Any) -> str:
        type_name = self._parse_type_by_target(value)[0]
        return f'{value}@frozenclass|type:{type_name};'

    def deep_freeze(self, class_: Callable) -> str:
        self._check_save_name()
        self.class_ = class_

        self._save_deep_data(self.class_)
        return self.save_name

    def _deep_parse_attributes(self, class_: Callable) -> dict:
        class_vars = class_.__dir__()
        res = {}
        for attribute_name in class_vars:
            attrib_value = getattr(class_, attribute_name)
            if not self.__is_bad_to_save(attrib_value, attribute_name):
                continue

            if self.__is_custom_class(attrib_value):
                res[attribute_name] = {
                    "var_name": attribute_name,
                    "var_type": self._parse_type_by_target(attrib_value)[0],
                    "var_type_import": self._parse_type_by_target(attrib_value)[1],
                    "var_value": self._deep_parse_attributes(attrib_value),
                }
            else:
                res[attribute_name] = {
                    "var_name": attribute_name,
                    "var_type": self._parse_type_by_target(attrib_value)[0],
                    "var_type_import": self._parse_type_by_target(attrib_value)[1],
                    "var_value": attrib_value,
                }
        return res

    def __is_bad_to_save(self, target: Any, attribute_name: str) -> bool:
        """True if it is  not baneed value"""
        if callable(target):
            for banned_tag in BAD_SAVE_PHRASES:
                if banned_tag in str(type(target)):
                    return False

        if attribute_name in BANNED_VAR_NAMES:
            return False

        if target is None:
            return False

        return True

    def __is_custom_class(self, target: Any) -> bool:
        """Return True if it if custom class"""
        if len(self._parse_type_by_target(target)[1].split('.')) == 1:
            return False
        return True

    def _save_deep_data(self, target_class: Callable) -> None:
        attributs = self._deep_parse_attributes(target_class)
        attributs = self.__vars_filter(attributs)

        attributs = self.__remake_dict_keys(attributs)

        self.__save_by_data(attributs)


    def __vars_filter(self, vars: dict) -> dict:
        new_attr = {}
        for banned_var in BANNED_VAR_NAMES:
            vars.pop(banned_var, None)

        for var_name in vars:
            if vars[var_name]["var_type"] != "NoneType":
                new_attr[var_name] = vars[var_name]

        return new_attr

    def __remake_dict_keys(self, attributs: dict) -> dict:
        for var_name in attributs:
            if attributs[var_name]['var_type'] == 'dict':
                attributs[var_name]['var_value'] = \
                    self.__add_marks_for_dict(attributs[var_name]['var_value'])
        return attributs

    def __save_by_data(self, data: dict, recursion_num: int = 0) -> None:
        if recursion_num == 0:
            res = GLOBAL_TEMPLATE.format(
                save_name=self.save_name,
                saved_class=self._parse_type_by_target(self.class_)[0],
                class_path=self._parse_type_by_target(self.class_)[1],
                class_parents=get_json_bases_data_by_class(self.class_),
            )

            for attrname in data:
                res += "\n"
                if data[attrname]['var_type_import'] not in STANDART_TYPES:
                    self.__save_by_data(data[attrname], recursion_num + 1)
                    new_attrs = data[attrname]
                    new_attrs['var_value'] = f'@frozenclass|saved_data?{self.save_name}:{recursion_num + 1}'
                    res += VAR_TEMPLATE.format(**new_attrs)
                elif data[attrname]['var_type'] in JSON_FORMATS:
                    new_attr = deepcopy(data[attrname])
                    new_attr['var_value'] = json.dumps(new_attr['var_value'])

                    res += VAR_TEMPLATE.format(**new_attr)
                else:
                    res += VAR_TEMPLATE.format(**data[attrname])

        else:
            res = GLOBAL_TEMPLATE.format(
                save_name=f'{self.save_name}:{recursion_num}',
                saved_class=data['var_type'],
                class_path=data['var_type_import'],
                class_parents=get_json_bases_data_by_class(
                    get_type_by_saved_type(data["var_type_import"])),
            )

            for attrname in data['var_value']:
                res += "\n"
                if data['var_value'][attrname]['var_type_import'] not in STANDART_TYPES:
                    self.__save_by_data(data['var_value'][attrname], recursion_num + 1)
                    new_attrs = data['var_value'][attrname]
                    new_attrs['var_value'] = f'@frozenclass|saved_data?{self.save_name}:{recursion_num + 1}'
                    res += VAR_TEMPLATE.format(**new_attrs)
                elif data['var_value'][attrname]['var_type'] in JSON_FORMATS:
                    new_attr = deepcopy(data['var_value'][attrname])
                    new_attr['var_value'] = json.dumps(new_attr['var_value'])

                    res += VAR_TEMPLATE.format(**new_attr)
                else:
                    res += VAR_TEMPLATE.format(**data['var_value'][attrname])



        if recursion_num == 0:
            with open(self.saved_path, 'w', encoding='utf-8') as filesave:
                filesave.write(res)
        else:
            new_save_path = (
                f"{self.saves_path}/{self.save_name}:{recursion_num}_"
                f"{str(datetime.now()).split()[0]}_{randint(10**10, 10**11)}.save"
            )
            with open(new_save_path, 'w', encoding='utf-8') as filesave:
                filesave.write(res)
