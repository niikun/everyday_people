# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project in its initial state. The repository contains only a `.gitignore` file configured for Python development with comprehensive exclusions for:
- Python bytecode and distribution files
- Virtual environments and package managers (pip, poetry, pdm, pixi, uv)
- Testing and coverage reports
- Development tools (mypy, ruff, pytest)
- IDE configurations (VS Code, PyCharm, Cursor)
- Documentation build artifacts

## Development Environment

This appears to be a new Python project. The `.gitignore` suggests support for multiple Python package managers and development tools:
- Standard Python tools (pip, setuptools)
- Modern package managers (poetry, pdm, pixi, uv)
- Code quality tools (ruff, mypy)
- Testing frameworks (pytest)

## Common Commands

Since this is a new project without a `package.json`, `pyproject.toml`, or other configuration files, specific build/test commands are not yet defined. Future instances should check for:
- `pyproject.toml` for poetry/pdm/uv projects
- `requirements.txt` for pip-based projects
- `Pipfile` for pipenv projects
- `Makefile` for custom build commands

## Architecture

The project structure has not yet been established. This is a blank Python project ready for initial development.