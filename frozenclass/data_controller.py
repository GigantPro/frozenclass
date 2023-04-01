from typing import Any, NoReturn
import os

from .dataparser import DataParser, DataWriter


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

    def change_saves_path(self, new_path: str, copy_old: bool = False) -> None:
        pass

    def freeze_class(
        self, target_class: Any, save_name: str = ...
    ) -> bool | NoReturn:  # type(...) == ellipsis
        if isinstance(save_name, type(...)):
            if hasattr(target_class, '__name__'):
                save_name = getattr(target_class, '__name__')

            else:
                save_name = None
        return DataWriter(self._saves_path, save_name).freeze_class(target_class)

    def load_save(self, save_name: str) -> Any:
        pass
