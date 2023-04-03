from copy import deepcopy
import json
from typing import Any, Callable
from random import randint
from datetime import datetime

from .types_modul import TypesModule
from .const import JSON_FORMATS, VAR_TEMPLATE, GLOBAL_TEMPLATE, BANNED_VAR_NAMES


class DataWriter:
    def __init__(self, saves_path: str, save_name: str | None = None) -> None:
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
                "var_type": self._parse_class_by_type(attrib_value)[0],
                "var_type_import": self._parse_class_by_type(attrib_value)[1],
                "var_value": attrib_value,
            }
        return res

    def _parse_class_by_type(self, target_: Any) -> tuple[str, str]:  # fix me 1
        str_type = str(type(target_))
        return str_type.split("'")[-2].split(".")[-1], str_type.split("'")[-2]

    def _create_save_data(self) -> str:
        res = GLOBAL_TEMPLATE.format(
            save_name=self.save_name,
            saved_class=self._parse_class_by_type(self.class_)[0],
            class_path=self._parse_class_by_type(self.class_)[1],
            class_parents=TypesModule().get_json_bases_data_by_class(self.class_),
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
            if self.parsed_attributes[var_name]["var_type"] != "NoneType":
                new_attr[var_name] = self.parsed_attributes[var_name]

        self.parsed_attributes = new_attr
