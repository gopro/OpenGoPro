# AGENTS.md - AI Agent Guidelines for Open GoPro Python SDK

This document provides guidelines for AI agents working on this Python SDK.

## Project Overview

**Open GoPro Python SDK** (`open_gopro`) is an asyncio-based Python library that provides an interface for controlling GoPro cameras via Bluetooth Low Energy (BLE) and WiFi/USB HTTP APIs.

### Key Technologies

- **Python**: 3.11 - 3.13
- **Package Manager**: [Poetry](https://python-poetry.org/)
- **Task Runner**: [Poe the Poet](https://poethepoet.naber.io/) (via `poetry run poe <task>`)
- **Testing**: pytest with pytest-asyncio
- **Type Checking**: mypy
- **Linting**: pylint
- **Formatting**: black, isort
- **Documentation**: Sphinx with Read the Docs theme

### Project Structure

```
open_gopro/           # Main package source
├── api/              # BLE and HTTP command definitions
├── database/         # COHN database implementation
├── demos/            # CLI demo applications
├── domain/           # Interfaces, enums, exceptions
├── features/         # High-level feature implementations
├── models/           # Data models, proto definitions, constants
├── network/          # BLE and WiFi communication layers
├── parsers/          # Response parsing logic
└── util/             # Logging and utilities

tests/
├── unit/             # Unit tests (mocked dependencies)
├── e2e/              # End-to-end tests (requires real camera)
├── conftest.py       # Shared pytest fixtures and mocks
└── mocks.py          # Mock implementations for testing

docs/                 # Sphinx documentation source
```

## Development Setup

### Initial Setup

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install all dependencies including dev and gui extras
poetry install --all-extras

# Activate the virtual environment
poetry shell
```

### Available Tasks

View all available tasks:

```bash
poetry run poe --help
```

Key tasks:

| Task | Command | Description |
|------|---------|-------------|
| `format` | `poetry run poe format` | Format code with black and sort imports with isort |
| `lint` | `poetry run poe lint` | Format, type check (mypy), and lint (pylint) |
| `tests` | `poetry run poe tests` | Run unit tests with coverage |
| `docs` | `poetry run poe docs` | Validate docstrings and build Sphinx documentation |
| `docstrings` | `poetry run poe docstrings` | Check docstring style (pydocstyle) and validity (pydoclint) |
| `all` | `poetry run poe all` | Run format, lint, tests, docs, and license check |
| `clean` | `poetry run poe clean` | Clean all build artifacts and caches |

## Unit Testing

### Running Tests

```bash
# Run all unit tests
poetry run poe tests

# Run with pytest directly for more control
poetry run pytest tests/unit

# Run a specific test file
poetry run pytest tests/unit/test_ble_commands.py

# Run a specific test
poetry run pytest tests/unit/test_ble_commands.py::test_specific_name

# Run with verbose output
poetry run pytest tests/unit -v

# Run with specific log level
poetry run pytest tests/unit --log-cli-level=DEBUG
```

### Test Configuration

- Tests use `pytest-asyncio` with `asyncio_mode = "auto"` - async tests are detected automatically
- Default timeout is 10 seconds per test
- Coverage threshold is **70%** minimum
- Test reports are generated in `.reports/`

### Writing Tests

- Unit tests go in `tests/unit/`
- Use fixtures from `tests/conftest.py` (e.g., `mock_wireless_gopro`, `mock_ble_communicator`)
- Mock implementations are in `tests/mocks.py`
- E2E tests require a physical camera and go in `tests/e2e/`

Example test structure:

```python
import pytest
from tests.mocks import MockWirelessGoPro

@pytest.mark.asyncio
async def test_something(mock_wireless_gopro):
    # Test implementation
    result = await mock_wireless_gopro.some_method()
    assert result is not None
```

## Linting and Code Quality

### Pre-Commit Checklist

**Always run before committing:**

```bash
poetry run poe lint
```

This runs:
1. `black` - Code formatting
2. `isort` - Import sorting
3. `mypy` - Type checking
4. `pylint` - Code linting

### Individual Checks

```bash
# Format code only
poetry run poe format

# Type checking only
poetry run poe _types

# Pylint only
poetry run poe _pylint
```

### Code Style Guidelines

- **Line length**: 120 characters (black configuration)
- **Import sorting**: black profile (isort)
- **Docstrings**: Google style convention
- **Type hints**: Required for all function signatures (mypy enforces)

### Mypy Configuration

- `disallow_untyped_defs = true` - All functions must have type hints
- `warn_unused_ignores = true` - Flag unnecessary type: ignore comments
- Uses `returns` plugin for functional error handling

### Pylint Configuration

- Ignores `tests/` and `proto/` directories
- Uses Google-style docstrings
- Max line length: 160 characters
- See `[tool.pylint.*]` sections in `pyproject.toml` for disabled checks

## Documentation

### Overview

Documentation uses **Sphinx** with the **Read the Docs theme** and is published at:
https://gopro.github.io/OpenGoPro/python_sdk/

### Building Documentation

```bash
# Full documentation build (validates docstrings first)
poetry run poe docs

# Build Sphinx docs only
poetry run poe sphinx

# Check docstrings only
poetry run poe docstrings
```

### Documentation Structure

- `docs/index.rst` - Main landing page
- `docs/api.rst` - API reference (auto-generated from docstrings)
- `docs/quickstart.rst` - Quick start guide
- `docs/usage.rst` - Detailed usage examples
- Built output goes to `docs/build/`

### Writing Docstrings

Use **Google-style docstrings**:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.

    Longer description if needed, explaining the behavior
    in more detail.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is invalid
    """
```

### Docstring Validation

Two tools validate docstrings:
- **pydocstyle**: Checks style conformance to Google convention
- **pydoclint**: Validates docstring completeness and accuracy

## Commits

### Conventional Commits

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring without behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks, dependencies |
| `ci` | CI/CD changes |

### Examples

```bash
feat(ble): add support for new camera model
fix(wifi): handle connection timeout correctly
docs(api): update docstrings for http_commands
test(unit): add tests for response parsing
refactor(parsers): simplify JSON response handling
chore(deps): update bleak to 2.1.1
```

### Commit Guidelines

- Keep commits atomic and focused
- Write clear, descriptive commit messages
- Reference issue numbers when applicable: `fix(api): resolve timeout issue (#123)`
- Update `CHANGELOG.rst` for user-facing changes

## CI/CD Integration

### Nox Sessions

The project uses [Nox](https://nox.thea.codes/) for CI testing across Python versions:

```bash
# Run all nox sessions
nox

# Run specific session
nox -s tests
nox -s lint
nox -s docs
```

### CI Workflow

GitHub Actions runs:
1. `format` - Check code formatting
2. `lint` - Type checking and linting
3. `tests` - Unit tests across Python 3.11, 3.12, 3.13
4. `docstrings` - Docstring validation
5. `docs` - Documentation build

## Additional Notes

### Error Handling

The project uses the [`returns`](https://returns.readthedocs.io/) library for functional error handling. Many methods return `Result` types instead of raising exceptions.

### Async/Await

All camera communication is async. Use `async with` for GoPro connections:

```python
async with WirelessGoPro() as gopro:
    await gopro.ble_command.some_command()
```

### Protocol Buffers

Proto files are in `open_gopro/models/proto/`. Generated `*_pb2.py` files should not be manually edited.

### Dependencies

- Check licenses before adding dependencies: `poetry run poe licenses`
- License report is saved to `thirdPartyDependencies.csv`

### Common Issues

1. **BLE connection issues**: Ensure Bluetooth is enabled and camera is discoverable
2. **Import errors**: Run `poetry install --all-extras` to install all dependencies
3. **Test timeouts**: Default timeout is 10s; use `@pytest.mark.timeout(30)` for longer tests
4. **Type errors**: The codebase uses strict typing; ensure all functions have type hints
