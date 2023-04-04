from typing import Any
import json
from copy import deepcopy

from .types_modul import TypesModule
from .const import JSON_FORMATS

types = TypesModule()


class DataParser:
    def __init__(self, filename: str) -> None:
        self.filename = filename

        self.saved_data = {}
        self._class = None

    def parse_file(self) -> Any:
        self.saved_data = self.parse_file_content()
        self._encoding_dict_keys()

        self._class = types.get_type_by_saved_type(self.saved_data["type"]["class_path"])

        if self._class:
            return types.create_class_instance(self._class, self.saved_data["var"])

        type_ = types.generate_class_by_info(self.saved_data)
        return types.create_class_instance(type_, self.saved_data["var"])

    def parse_file_content(self, file_name: str | None = None) -> dict[Any]:
        file_name = file_name if file_name else self.filename
        with open(file_name, "r", encoding="utf-8") as file:
            file_content = file.readlines()
        file_content = [x.strip() for x in file_content if x.strip() != ""]

        saved_data = {}
        now_name = None
        var = []
        temp_var = {}
        for line in file_content:
            if line[0] + line[-1] == "[]":
                now_name = line[1:-1]
                if now_name == "var" and temp_var:
                    var.append(temp_var)
                    temp_var = {}
                saved_data[now_name] = saved_data.get(now_name, {})
            else:
                name, value = line.split("=")
                if now_name == "var":
                    temp_var[name] = value
                else:
                    value = "=".join(value) if isinstance(value, list) else value
                    saved_data[now_name][name] = value
        if temp_var not in var:
            var.append(temp_var)
        saved_data["var"] = var

        new_vars = []
        for var in saved_data["var"]:
            _new_var_ = deepcopy(var)
            if var["var_type"] in JSON_FORMATS:
                _new_var_["var_value"] = json.loads(
                    _new_var_["var_value"]
                )  
            new_vars.append(_new_var_)

        saved_data["var"] = new_vars

        return saved_data

    def _encoding_dict_keys(self) -> None:
        res = []
        for var_decription in self.saved_data['var']:
            new_var = var_decription
            if var_decription['var_type'] == 'dict':
                new_value = {}
                for key in var_decription['var_value']:
                    if '@frozenclass|' not in key:
                        new_value[key] = var_decription['var_value'][key]
                        continue

                    new_value[self.__parse_value_name(key)] = \
                        var_decription['var_value'][key]
                new_var['var_value'] = new_value
            res.append(new_var)
        self.saved_data['var'] = res

    def __parse_value_name(self, key: str) -> str:
        key_value, description = key.split('@')
        new_key = ''

        name, args = description.split('|')
        if name != 'frozenclass':
            return key

        for specif in args.split(';'):
            if specif.strip() == '':
                continue

            spec_type, spec_value = specif.split(':')

            if spec_type == 'type':
                new_key = \
                    TypesModule().get_value_by_type(key_value, spec_value)
        return new_key
