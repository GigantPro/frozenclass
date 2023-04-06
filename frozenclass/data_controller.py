from typing import Any
import os
from shutil import copyfile

from .dataparser import DataParser, DataWriter
from .exceptions import NoSave


class DataController:
    """The main class of the library. Responsible for its functions."""

    def __init__(self, saves_folder_path: str) -> None:
        """__init__ method

        Args:
            saves_folder_path (str): Path to the folder where you plan to store/load classes
        """
        self._saves_path = saves_folder_path

        os.makedirs(self._saves_path, exist_ok=True)

    def get_all_saves(self) -> list[Any]:
        """Will return you instances of all previously saved classes.

        Returns:
            list[Any]: List of class instances.
        """
        list_dir = os.listdir(self._saves_path)
        classes_list = []

        for save in list_dir:
            classes_list.append(DataParser(f"{self._saves_path}/{save}", self).parse_file())

        return classes_list

    def change_saves_path(self, new_path: str, copy_old: bool = False) -> None:
        """Changes the path where the saves are stored, and, if necessary, moves the old saves there.
        Be careful, the next time you create a DataController, you will need to specify a new class path.

                Args:
                    new_path (str): New save folder path;
                    copy_old (bool, optional): New save folder path. Defaults to False.
        """
        os.makedirs(new_path, exist_ok=True)

        if copy_old:
            list_dir = os.listdir(self._saves_path)
            for save in list_dir:
                copyfile(f"{self._saves_path}/{save}", f"{new_path}/{save}")
            os.system(f"rm -rf {self._saves_path}")

        self._saves_path = new_path

    def freeze_class(self, target_class: Any, save_name: str = ...) -> str:
        """Used to save a class to a file

        Args:
            target_class (Any): The class to be saved
            save_name (str, optional): The key by which it will be possible to obtain the saved class in the future.
            It is also displayed in the name of the file with saving. Defaults to ...

        Returns:
            str: Save name
        """
        if isinstance(save_name, type(...)):
            if hasattr(target_class, "__name__"):
                save_name = getattr(target_class, "__name__")

            else:
                save_name = None
        return DataWriter(self._saves_path, save_name).freeze_class(target_class)

    def load_save(self, save_name: str) -> Any:
        """Needed to load a save with a specific save name

        Args:
            save_name (str): The name of the desired save

        Raises:
            NoSave: If there is no save with the given name

        Returns:
            Any: The instance of the class that was saved
        """
        list_dir = os.listdir(self._saves_path)

        for save_filename in list_dir:
            parser = DataParser(f"{self._saves_path}/{save_filename}", self)
            parsed_content = parser.parse_file_content()
            if parsed_content["SavedModel"]["save_name"] == save_name:
                return parser.parse_file()
        raise NoSave("save_name")

    def deep_freeze(self, target_class: Any, save_name: str = ...) -> str:
        if isinstance(save_name, type(...)):
            if hasattr(target_class, "__name__"):
                save_name = getattr(target_class, "__name__")

            else:
                save_name = None
        return DataWriter(self._saves_path, save_name).deep_freeze(target_class)
