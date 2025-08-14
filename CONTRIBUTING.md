# Contributing to Energy Counters Library

Thank you for considering contributing to the Energy Counters Library! This document provides guidelines and information for contributors.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Code Style and Conventions](#code-style-and-conventions)
- [Contributing Process](#contributing-process)
- [Implementing New Counter Support](#implementing-new-counter-support)
- [Testing Guidelines](#testing-guidelines)
- [Issue Reporting](#issue-reporting)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Documentation Standards](#documentation-standards)

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Text editor or IDE of your choice

### Installation for Development

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/energy-counters.git
   cd energy-counters
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

4. **Install recommended development tools:**
   ```bash
   pip install -r dev-requirements.txt
   ```

5. **Optional: Set up pre-commit hooks for code quality:**
   ```bash
   pre-commit install
   ```

### Recommended Development Tools

- **Code Formatting:** [Black](https://black.readthedocs.io/)
- **Linting:** [Flake8](https://flake8.pycqa.org/)
- **Type Checking:** [MyPy](http://mypy-lang.org/)
- **Import Sorting:** [isort](https://pycqa.github.io/isort/)
- **Pre-commit Hooks:** [Pre-commit](https://pre-commit.com/) (optional but recommended)

All development dependencies are listed in `dev-requirements.txt` for easy installation.

## Code Style and Conventions

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters (Black default)
- Use type hints for all function parameters and return values
- Use descriptive variable and function names

### Formatting Commands

```bash
# Format code with Black
black src/

# Check code style with Flake8
flake8 src/

# Sort imports with isort
isort src/

# Type checking with MyPy
mypy src/energy_counters/
```

### Naming Conventions

- **Classes:** PascalCase (e.g., `EM530DataCollector`)
- **Functions/Methods:** snake_case (e.g., `collect_data`)
- **Variables:** snake_case (e.g., `counter_config`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)
- **Files:** snake_case (e.g., `em530.py`)

## Contributing Process

### 1. Before Starting

- Check existing [issues](https://github.com/nobrega8/energy-counters/issues) and [pull requests](https://github.com/nobrega8/energy-counters/pulls)
- For major changes, open an issue first to discuss the proposed changes
- Ensure your contribution aligns with the project's goals

### 2. Making Changes

- Create a new branch from `master`: `git checkout -b feature/your-feature-name`
- Make your changes following the code style guidelines
- Test your changes thoroughly
- Update documentation as needed

### 3. Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Keep the first line under 50 characters
- Provide additional details in the commit body if needed

Example:
```
Add support for Schneider IEM3250 energy meter

- Implement ModbusDataCollector for IEM3250
- Add register mapping and data formatting
- Include comprehensive error handling
- Update documentation with usage examples
```

## Implementing New Counter Support

### Counter Implementation Structure

Each counter implementation should follow this structure:

```
src/energy_counters/brand_name/
├── __init__.py
├── README.md
├── counter_model.py
└── (additional models as needed)
```

### Required Components

1. **Data Collector Class:**
   ```python
   class CounterModelDataCollector:
       """Brief description of the counter"""
       
       def __init__(self, counter_config: CounterConfiguration, 
                    modbus_tcp_config: Optional[ModbusTCPConfiguration] = None,
                    modbus_rtu_config: Optional[ModbusRTUConfiguration] = None):
           # Implementation
       
       def connect(self) -> bool:
           # Connection logic
       
       def collect_data(self) -> Optional[Dict[str, Any]]:
           # Data collection logic
       
       def disconnect(self) -> None:
           # Disconnection logic
   ```

2. **Configuration Classes:**
   - Use existing `CounterConfiguration`, `ModbusTCPConfiguration`, `ModbusRTUConfiguration` from `common.configurations`

3. **Data Formatting:**
   - Return standardized data format with consistent field names
   - Include timestamp, counter identification, and measurement values
   - Handle unit conversions and scaling factors

### Implementation Checklist

- [ ] Create counter module directory structure
- [ ] Implement data collector class with required methods
- [ ] Add Modbus register mapping and data parsing
- [ ] Implement error handling and logging
- [ ] Support both TCP and RTU protocols when possible
- [ ] Create comprehensive README.md with:
  - [ ] Counter specifications
  - [ ] Modbus register map
  - [ ] Usage examples
  - [ ] Configuration parameters
- [ ] Update main README.md supported counters table
- [ ] Add import to package `__init__.py`

### Register Mapping Documentation

Document register mappings in the counter's README.md:

```markdown
#### Modbus Register Map

| Register Address | Register Count | Data Type | Scale Factor | Description |
|------------------|----------------|-----------|--------------|-------------|
| 4001-4002 | 2 | uint32be | 0.1 | Voltage L1 (V) |
| 4003-4004 | 2 | uint32be | 0.001 | Current L1 (A) |
```

## Testing Guidelines

### Manual Testing

Since there's no formal test framework currently:

1. **Test with actual hardware when possible**
2. **Create test scripts in the counter's main function:**
   ```python
   def main():
       """Main function for testing"""
       # Example configuration for testing
       counter_config = CounterConfiguration(...)
       # Test implementation
   ```

3. **Validate data collection:**
   - Verify all expected fields are present
   - Check data types and formats
   - Test error handling scenarios
   - Validate both TCP and RTU connections

### Testing Checklist

- [ ] Connection establishment (TCP and RTU)
- [ ] Data collection and parsing
- [ ] Error handling (connection failures, invalid responses)
- [ ] Data format consistency
- [ ] Configuration validation
- [ ] Disconnection and cleanup

## Issue Reporting

### Bug Reports

When reporting bugs, include:

- **Description:** Clear description of the issue
- **Steps to Reproduce:** Detailed steps to reproduce the problem
- **Expected Behavior:** What you expected to happen
- **Actual Behavior:** What actually happened
- **Environment:**
  - Python version
  - Library version
  - Operating system
  - Counter model and configuration
- **Error Messages:** Full error messages and stack traces
- **Additional Context:** Any other relevant information

### Feature Requests

For feature requests, include:

- **Description:** Clear description of the desired feature
- **Use Case:** Why this feature would be useful
- **Proposed Solution:** If you have ideas for implementation
- **Alternatives:** Alternative solutions you've considered

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] Changes have been tested manually
- [ ] Documentation has been updated
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with master branch

### Pull Request Description

Include in your PR description:

- **Summary:** Brief description of changes
- **Motivation:** Why these changes are needed
- **Changes Made:** List of specific changes
- **Testing:** How the changes were tested
- **Screenshots:** If applicable (for documentation changes)

### Review Process

1. **Automated Checks:** Ensure all automated checks pass
2. **Code Review:** Address any feedback from reviewers
3. **Testing:** Verify changes work as expected
4. **Documentation:** Ensure documentation is complete and accurate

## Documentation Standards

### README Files

Each counter module should have a comprehensive README.md with:

- **Overview:** Brief description of the counter
- **Features:** Supported capabilities
- **Installation:** Any specific requirements
- **Usage Examples:** Complete working examples
- **Configuration:** All configuration options
- **Register Map:** Detailed Modbus register documentation
- **Troubleshooting:** Common issues and solutions

### Code Documentation

- Use docstrings for all classes, methods, and functions
- Follow [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Include parameter types and descriptions
- Document return values and exceptions

Example:
```python
def collect_data(self) -> Optional[Dict[str, Any]]:
    """Collect data from the energy counter.
    
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing counter data with
            standardized field names, or None if collection fails.
            
    Raises:
        ConnectionError: If unable to establish connection to counter.
        ModbusException: If Modbus communication fails.
    """
```

## Getting Help

- **Issues:** Open an [issue](https://github.com/nobrega8/energy-counters/issues) for bugs or feature requests
- **Discussions:** Use GitHub Discussions for questions and community support
- **Documentation:** Check existing counter implementations for examples

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing to the Energy Counters Library! Your contributions help make this tool better for everyone working with industrial energy monitoring systems.