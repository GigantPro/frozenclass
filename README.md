# Warning: project is unstable now. At the moment, the library has just begun to be developed, so this is not the final form of the product!



# pysavedata 
This library was created in order to be able to save classes with a single line, as well as load them!



## Examples
```python 
from pysavedata import DataController


# Init controller class
data_controller = DataController('PATH_TO_SAVE`S FOLDER')

# Get all saves classes models
loaded_classes = data_controller.get_all_saves_list()  # -> list[classes models]
```

## Installation

```bash
$ pip install pysavedata
```

## Installation from source

Dependencies:
- poetry
```bash
$ git clone https://github.com/GigantPro/pysavedata.git
$ poetry run build_pkg
$ pip install "dist/pysavedata-0.0.2a0.tar"
```