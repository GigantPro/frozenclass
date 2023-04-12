<p align="center">
        <h1 align="center">FrozenClass</h1>
        <h2 align="center">This library was created in order to be able to save classes with a single line, as well as load them!</h2>
</a>



<p align="center">
        <a href="https://pypi.python.org/pypi/frozenclass"><img alt="Pypi version" src="https://img.shields.io/pypi/v/frozenclass.svg"></a>
        <a href="https://pypi.python.org/pypi/frozenclass"><img alt="Python versions" src="https://img.shields.io/badge/python-3.7+ | PyPy-blue.svg"></a>
        <img alt="Size" src="https://img.shields.io/github/languages/code-size/GigantPro/frozenclass">
        <a href="https://pypi.org/project/frozenclass/"><img alt="Pypi version" src="https://img.shields.io/pypi/l/frozenclass?color=orange"></a>
</p>
<p align="center">
        <a href="https://github.com/GigantPro/frozenclass/actions/workflows/tests.yml"><img alt="Testing status" src="https://github.com/GigantPro/frozenclass/actions/workflows/tests.yml/badge.svg?branch=main"></a>
        <a href="https://github.com/GigantPro/frozenclass/actions/workflows/linting.yml"><img alt="Linting" src="https://github.com/GigantPro/frozenclass/actions/workflows/linting.yml/badge.svg?branch=main"></a>
</p>





## Example
```python 
from frozenclass import DataController


# Test class
class Test:
    test_var = 10


# Init controller class
data_controller = DataController('PATH_TO_SAVE`S FOLDER')

# Save class as file
save_name = data_controller.freeze_class(Test())

# Get all saves classes models
loaded_classes = data_controller.load_save(save_name)  # -> Test object

# Get var value
print(test_var.test_var) # -> 10
```

## Installation

```bash
$ pip install frozenclass
```

## Installation from source

### Dependencies:
- **poetry**
```bash
$ git clone https://github.com/GigantPro/frozenclass.git; cd frozenclass-main
$ poetry run build; cd dist
$ pip install $(ls -Art | tail -n 1)
```
