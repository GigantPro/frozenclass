from typing import Any

from .types_modul import TypesModule

types = TypesModule()


class DataParser:
    def __init__(self, filename: str) -> None:
        self.filename = filename

        self.saved_data = {}
        self._class = None

    def parse_file(self) -> Any:
        file_content = None
        with open(self.filename, 'r', encoding='utf-8') as file:
            file_content = file.readlines()
        file_content = [x.strip() for x in file_content if x.strip() != '']

        now_name = None
        var = []
        temp_var = {}
        for line in file_content:
            if line[0] + line[-1] == '[]':
                now_name = line[1:-1]
                if now_name == 'var' and temp_var:
                    var.append(temp_var)
                    temp_var = {}
                self.saved_data[now_name] = self.saved_data.get(now_name, {})
            else:
                name, value = line.split('=')
                if now_name == 'var':
                    temp_var[name] = value
                else:
                    value = '='.join(value) if isinstance(value, list) else value
                    self.saved_data[now_name][name] = value
        self.saved_data['var'] = var


        self._class = types.get_type_by_saved_type(self.saved_data['type'])

        if self._class:
            return types.create_class_instance(self._class, self.saved_data['var'])

        type_ = types.generate_class_by_info(self.saved_data)
        return types.create_class_instance(type_, self.saved_data['var'])
