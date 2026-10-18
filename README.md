# Match Library Manager

A Python application for managing soccer match directories.

The application reads match information from CSV files and maintains
organized match libraries for multiple teams.

## Features

Planned functionality includes:

- Configuration through TOML
- Support for multiple teams and match libraries
- Import and consolidation of match data from CSV files
- Consistent match directory naming
- Detection of existing directories
- Creation and renaming of match directories
- Dry-run mode to preview filesystem changes

## Requirements

- Python 3.12 or newer

## Configuration

Team profiles, source files, and library directories will be
configured in `Config.toml`.

## Status

Initial project setup. Application functionality is under development.

```bash
Match_Library_Manager/
│
├── Core/
│   ├── __init__.py
│   ├── Config.py           # Read and validate TOML configuration
│   ├── Match.py            # Represent match data
│   └── Match_Library.py    # Create and rename directories
│
├── Tests/
│   └── __init__.py
│
├── Match_Library_Manager.py
├── Config.toml
├── README.md
└── .gitignore

```
