from typing import Any, Optional, Union, Dict
import json
from copy import deepcopy

from .types_module import (
    get_type_by_saved_type,
    create_class_instance,
    generate_class_by_info,
    get_value_by_type,
)
from .const import JSON_FORMATS


class DataParser:
    def __init__(self, filename: str, data_controller_obj) -> None:
        self.filename = filename
        self.data_controller_obj = data_controller_obj

        self.saved_data = {}
        self._class = None

    def parse_file(self) -> Any:
        self.saved_data = self.parse_file_content()
        self._encoding_dict_keys()
        self.saved_data = self._encoding_deep_keys(self.saved_data)

        self._class = get_type_by_saved_type(self.saved_data["type"]["class_path"])

        if self._class:
            return create_class_instance(self._class, self.saved_data["var"])

        type_ = generate_class_by_info(self.saved_data)
        return create_class_instance(type_, self.saved_data["var"])

    def parse_saved_args(self) -> Dict[str, Any]:
        self.saved_data = self.parse_file_content()
        self._encoding_dict_keys()
        self.saved_data = self._encoding_deep_keys(self.saved_data)
        return self._get_vars_from_saved_data(self.saved_data)

    def _get_vars_from_saved_data(self, saved_data: dict) -> Dict[str, Any]:
        if saved_data['var'] is None:
            return {}

        res = {}
        for var_desc in saved_data['var']:
            res[var_desc['var_name']] = get_value_by_type(var_desc['var_value'], var_desc['var_type'])
        return res

    def parse_file_content(self, file_name: Optional[str] = None) -> Union[Dict, None]:
        file_name = file_name if file_name else self.filename
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                file_content = file.readlines()
            except UnicodeDecodeError:
                return None
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
                    get_value_by_type(key_value, spec_value)
        return new_key

    def _encoding_deep_keys(self, data: dict) -> dict:
        new_var_desc = []
        for var_desc in data['var']:
            if '@frozenclass|' in var_desc['var_value']:
                var_desc['var_value'] = var_desc['var_value'][13:]
                name_, value_ = var_desc['var_value'].split('?')

                if name_ == 'saved_data':
                    var_desc['var_value'] = self.data_controller_obj.load_save(value_)
            new_var_desc.append(var_desc)
        data['var'] = new_var_desc
        return data
