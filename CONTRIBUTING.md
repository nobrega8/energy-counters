# Contributing to Energy Counters Library

Thank you for your interest in contributing to the **Energy Counters Library**! This guide explains how to get started, submit contributions, and maintain consistency across the project.

---

## Table of Contents

- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Adding Support for a New Counter](#adding-support-for-a-new-counter)
- [Code Style](#code-style)
- [Testing](#testing)
- [Commits & Pull Requests](#commits--pull-requests)
- [Issues & Bug Reports](#issues--bug-reports)
- [Contact](#contact)

---

## Requirements

- Python **3.8+**
- [`pymodbus`](https://github.com/riptideio/pymodbus) ≥ 3.0.0
- [`pyserial`](https://pyserial.readthedocs.io/en/latest/) ≥ 3.5

Ensure you have a recent version of `pip`, `venv`, and `setuptools`.

---

## Getting Started

1. **Fork** this repository and **clone** your fork:

   ```bash
   git clone https://github.com/<your-username>/energy-counters.git
   cd energy-counters
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install in development mode**:

   ```bash
   pip install -e .[dev]
   ```

4. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## Adding Support for a New Counter

To add support for a new energy meter:

1. **Create a new folder** inside `src/energy_counters/` for the brand (if it doesn’t exist already).  
   Example: `src/energy_counters/schneider/`

2. **Create a data collector class** (e.g., `IEM3250DataCollector`) that extends `BaseDataCollector`.

3. Implement the required methods:
   - `connect()`
   - `collect_data()`
   - `disconnect()`

4. **Use the appropriate Modbus protocol** (RTU or TCP) via the `pymodbus` client.

5. **Return data as a dictionary**, using a consistent naming format:

   ```python
   {
       "voltageL1": 230.5,
       "currentL1": 5.2,
       "activePower": 1.21,
       ...
   }
   ```

6. **Update the main README** table to include your new counter.

---

## Code Style

- Follow **PEP8** style guidelines.
- Use **type hints** wherever possible.
- Organize files per manufacturer.
- Use **f-strings** for string formatting.
- Document all public methods with docstrings.

You can use tools like `flake8`, `black`, or `ruff` to check formatting.

---

## Testing

Preferably, test with actual hardware. Otherwise:

- Use mocks to simulate Modbus devices.
- Use `pytest` or `unittest` for writing automated tests.
- Ensure **existing functionality is not broken**.

To run all tests:

```bash
pytest
```

---

## Commits & Pull Requests

Follow [conventional commits](https://www.conventionalcommits.org/) when possible:

```
feat: add support for Schneider IEM3250
fix: correct power reading on DMG210
docs: update usage example for Carlo Gavazzi
```

Before submitting a **Pull Request**:

- Test your changes locally.
- Ensure your code follows the style guide.
- Update documentation or README files if needed.
- Provide a clear description of your changes.

---

## Issues & Bug Reports

Found a bug or unexpected behavior?

1. Search existing [issues](https://github.com/nobrega8/energy-counters/issues).
2. If not listed, create a new one including:
   - Brand and model of the meter
   - Communication method (RTU/TCP)
   - Description of the issue
   - Log output or traceback (if available)

---

## Contact

If you have questions or ideas, open an issue or reach out to the maintainer:

- GitHub: [@nobrega8](https://github.com/nobrega8)

We appreciate your contributions — thank you for helping improve Energy Counters!

---
