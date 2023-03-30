from typing import Any


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
        for line in file_content:
            print(f'{line=}')
            if line[0] + line[-1] == '[]':
                now_name = line.lstrip('[').rstrip(']')
                self.saved_data[now_name] = {}
            else:
                name, value = line.split('=')
                self.saved_data[now_name][name] = value


if __name__ == '__main__':
    print(DataParser('saves/123').__class__)
