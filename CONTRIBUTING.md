# Contributing Guide

Thank you for your interest in contributing to the project! This document provides guidelines and instructions to help you contribute effectively.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Environment Setup

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone [REPOSITORY_URL]
   cd pydoll
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Development Workflow

1. Create a new branch for your contribution:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or
   ```bash
   git checkout -b fix/your-fix-name
   ```

2. Make your changes following the code and testing guidelines.

3. Check your code using the linter:
   ```bash
   poetry run task lint
   ```

4. Format your code:
   ```bash
   poetry run task format
   ```

5. Run the tests to ensure everything is working:
   ```bash
   poetry run task test
   ```

6. Commit your changes following the commit conventions (see below).

7. Push your changes and open a Pull Request.

## Code Standards

This project uses [Ruff](https://github.com/charliermarsh/ruff) for linting and code formatting. The code standards are defined in the `pyproject.toml` file.

### Linting and Formatting

To check if your code follows the standards:

```bash
poetry run task lint
```

To automatically fix some issues and format your code:

```bash
poetry run task format
```

**Important:** Make sure to resolve all linting issues before submitting your changes. Code that doesn't pass the linting checks will not be accepted.

## Testing

### Writing Tests

For each new feature or modification, it is **mandatory** to write corresponding tests. We use `pytest` for testing.

- Tests should be placed in the `tests/` directory
- Test file names should start with `test_`
- Test function names should start with `test_`

### Running Tests

To run all tests:

```bash
poetry run task test
```

This will also generate a code coverage report (HTML) that can be viewed in the `htmlcov/` folder.

## Commit Messages

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) standard for commit messages. We use the `commitizen` tool to facilitate the creation of standardized commits.

### Commit Message Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation-only changes
- **style**: Changes that do not affect the meaning of the code (whitespace, formatting, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding or correcting tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files
- **chore**: Other changes that don't modify src or test files

### Examples of Good Commit Messages

```
feat(parser): add ability to parse arrays
```

```
fix(networking): resolve connection timeout issue

A problem was identified in the networking library that
caused unexpected timeouts. This change increases the
default timeout from 10s to 30s.
```

## Pull Request Process

1. Verify that your code passes all tests and linting checks.
2. Push your branch to the repository.
3. Open a Pull Request to the main branch.
4. In the PR description, clearly explain what was changed and why.
5. Link any related issues to your PR.
6. Wait for the code review. Read the comments and make necessary changes.

## Questions?

If you have questions or need help, open an issue in the repository or contact the project maintainers.

---

We appreciate your contributions to make this project better! 