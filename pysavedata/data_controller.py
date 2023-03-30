from typing import Any, NoReturn
import os

from .dataparser import DataParser


class DataController:
    def __init__(self, saves_folder_path: str) -> None:
        self._saves_path = saves_folder_path
        
        os.makedirs(self._saves_path, exist_ok=True)
        
    def get_all_saves_list(self) -> list[Any]:
        list_dir = os.listdir(self._saves_path)
        classes_list = []

        for save in list_dir:
            classes_list.append(DataParser(f'{self._saves_path}/{save}').parse_file())

        return classes_list

    def change_saves_path(self, new_path: str, copy_old: bool = False) -> None | NoReturn:
        pass
    
    def save_class(self, target_class: Any, save_name: str = ...) -> bool | NoReturn:  # type(...) == ellipsis
        pass
    
    def load_save(self, save_name: str) -> Any:
        pass

    
if __name__ == '__main__':
    DataController('saves').get_all_saves_list()
