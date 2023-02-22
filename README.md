# Yndx-parse

Yndx-parse is a Python library for parsing weather data.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Yndx-parse.

```bash
pip install yndx-parse
```

## Usage

```python
from yndx-parse import YndxParse

# Create an instance of the class,
# passing the argument as the name of the city.
yp = YndxParse('London')
print(yp.get_weather())

# Create an instance of the class,
# passing the argument as a tuple
# containing longitude and latitude.
coords = (54.341, 43.8766)
yp = YndxParse(coords)
print(yp.get_weather())
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
