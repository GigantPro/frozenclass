import configparser
from typing import Any


class DataReader(dict):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename = filename

        self.config = configparser.ConfigParser()

    def read_file(self) -> Any:
        pass

    def write_config(self) -> None:
        pass
