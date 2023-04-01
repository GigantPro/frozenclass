# Warning: project is unstable now. At the moment, the library has just begun to be developed, so this is not the final form of the product!



# frozenclass 
This library was created in order to be able to save classes with a single line, as well as load them!



## Example
```python 
from frozenclass import DataController


# Test class
class Test:
    pass


# Init controller class
data_controller = DataController('PATH_TO_SAVE`S FOLDER')

# Save class as file
data_controller.freeze_class(Test())

# Get all saves classes models
loaded_classes = data_controller.get_all_saves_list()  # -> list[class instances]
```

## Installation

```bash
$ pip install frozenclass
```

## Installation from source

Dependencies:
- poetry
```bash
$ git clone https://github.com/GigantPro/frozenclass.git
$ poetry run build
$ pip install "dist/frozenclass-0.0.3a0.tar"
```