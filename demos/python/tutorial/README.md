# Python Tutorials

This package is designed to be used with the accompanying Python [tutorials](https://gopro.github.io/OpenGoPro/tutorials/).

If you are a user of the tutorials, please visit the above link. Developer's of these tutorials can continue reading.

# Developer Information

## Tutorial Documentation

Each tutorial shall be documented via [Jekyll](../../../docs/tutorials/_python-tutorials). See the top-level
Docs [README](../../../docs/README.md) for more information.

## Tutorial Examples

Each tutorial shall contain an accompanying sample script in the `tutorial_modules` folder here. This script
shall be tested as detailed below.

## Linting

There should be no static typing or linting errors as checked via:

```
make lint
```

## Testing

Each script shall be tested via pytest by adding a case to the `tests/test_tutorials.py` file.

Tests can be run via:

```
make tests
```

After running th tests, test logs and a summary test report can be found in the `reports` folder.