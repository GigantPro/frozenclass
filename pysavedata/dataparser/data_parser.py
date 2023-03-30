from typing import Any

from .types_modul import TypesModule


class DataParser:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def parse_file(self) -> Any:
        file_content = None
        with open(self.filename, 'r', encoding='utf-8') as file:
            file_content = file.readlines()
        file_content = [x.strip() for x in file_content if x.strip() != '']
        
        self.saved_data = {}
        
        now_name = None
        var_val = var_type = var_name = None
        for line in file_content:
            if line[0] + line[-1] == '[]':
                if now_name and (var_type and var_name and var_val):
                    self.saved_data['var'][var_name] = TypesModule.get_value_by_type(var_val, var_type)
                    var_val = var_type = var_name = None
                
                now_name = line[1:-1]
                self.saved_data[now_name] = self.saved_data.get(now_name, {})
            else:
                name, value = line.split('=')
                value = '='.join(value) if isinstance(value, list) else value
                
                if now_name == 'var':
                    if name == 'var_name':
                        var_name = value
                    elif name == 'var_type':
                        var_type = value
                    elif name == 'var_value':
                        var_val = value

                elif now_name == 'type':
                    if name == 'saved_class':
                        self.saved_data['type']['saved_class'] = value

                else:
                    self.saved_data[now_name][name] = value
        if now_name and (var_type and var_name and var_val):
            self.saved_data['var'][var_name] = TypesModule.get_value_by_type(var_val, var_type)
        
        self._class = TypesModule.get_type_by_name(self.saved_data['type']['saved_class'])
        if self._class:
            return TypesModule.create_class_with_data(self._class, self.saved_data['var'])
        return TypesModule.generate_class_by_info(self.saved_data)
