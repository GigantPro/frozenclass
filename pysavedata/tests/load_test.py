import unittest

from .. import DataController
from .funcs import generate_test_file, check_res



class TestLoadFunc(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = DataController('saves')
        self.text, self.args = generate_test_file()

        with open('saves/load_test.save', 'w', encoding='utf-8') as file:
            file.write(self.text)

    def test_load(self):
        print(123123)
        res = self.controller.get_all_saves_list()
        self.assertTrue(check_res(res, self.args))

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
    