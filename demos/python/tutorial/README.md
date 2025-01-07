# Python Tutorials

This package is designed to be used with the accompanying Python [tutorials](https://gopro.github.io/OpenGoPro/tutorials/).

If you are a user of the tutorials, please visit the above link. Developer's of these tutorials should continue reading.

# Developer Information

## Development Environment Setup

With Python >= 3.10 and < 3.13, perform:

```
poetry install
```

## Tutorial Documentation

Each tutorial shall be documented via [Jekyll](../../../docs/tutorials/tutorials). See the top-level
Docs [README](../../../docs/README.md) for more information.

## Tutorial Examples

Each tutorial shall contain an accompanying sample script in the `tutorial_modules` folder here. This script
shall be tested as detailed below.

## Linting

There should be no static typing or linting errors as checked via:

```
poetry run poe lint
```

## Testing

Each script shall be tested via pytest by adding a case to the `tests/testtutorials.py` file.

Tests can be run via:

```
poetry run poe tests
```

After running the tests, test logs and a summary test report can be found in the `.reports` folder.