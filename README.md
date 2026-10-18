# Match Library Manager

A Python utility for creating and maintaining organized soccer match directories.

Match Library Manager reads match data from CSV files and creates or updates directory names based on available match information. It supports multiple teams, each with its own CSV source and library location.

## Features

- TOML-based configuration
- Support for multiple teams and independent match libraries
- Enable or disable individual teams
- Read match data from CSV files
- Create directories for upcoming matches with limited information
- Generate consistent directory names using dates, teams, results, and scores
- Support regular-season matches, playoffs, friendlies, and penalty shootouts
- Rename existing directories when match information changes
- Support multiple matches on the same date against different opponents
- Preserve existing files when renaming directories
- Detect ambiguous directory matches and report conflicts
- Dry-run mode to preview changes without modifying the filesystem
- Display processing summaries, warnings, and errors using Rich

## Requirements

- Python 3.11 or newer
- Dependencies listed in `requirements.txt`

Install dependencies:

```cmd
python -m pip install -r requirements.txt
```

## Configuration

Copy `Config.example.toml` to `Config.toml` and update the configuration for your environment.

Each team has its own name, enabled status, CSV source file, and output directory.

Example:

```toml
[General]
Dry_Run = true

[Teams.ATLUTD]
Team_Name = "Atlanta United"
Enabled = true
Library_Directory = 'D:\Soccer\ATLUTD\Games'
Source_File = 'D:\Soccer\Data\ATLUTD_Matches.csv'

[Teams.ATLUTD2]
Team_Name = "Atlanta United 2"
Enabled = false
Library_Directory = 'D:\Soccer\ATLUTD2\Games'
Source_File = 'D:\Soccer\Data\ATLUTD2_Matches.csv'
```

### Configuration options

| Setting | Description |
|---|---|
| `Dry_Run` | Preview directory creation and renaming without making changes |
| `Team_Name` | Team name used when generating directory names |
| `Enabled` | Include or exclude the team from processing |
| `Library_Directory` | Root directory for the team's match library |
| `Source_File` | CSV file containing the team's match records |

Both absolute and relative directory paths are supported. Relative paths are resolved from the project directory.

Windows paths can use forward slashes in double-quoted strings or backslashes in single-quoted TOML strings.

`Config.toml` is excluded from Git so machine-specific paths are not committed.

## Running the Application

Run:

```cmd
python Match_Library_Manager.py
```

The application processes each enabled team.

**Preview changes first** by setting:

```toml
Dry_Run = true
```

After reviewing the proposed changes, set `Dry_Run = false` to apply them.

The terminal displays directory creations, renames, conflicts, warnings, and a processing summary. Unchanged directories are counted but not individually displayed.

## Directory Structure

Match directories are organized by year within each team's library.

Example:

```text
Games/
├── 2026/
│   ├── 2026-10-10 - FC Cincinnati at Atlanta United, L 1-3/
│   └── 2026-10-17 - Atlanta United at Inter Miami, L 0-4/
└── 2027/
    └── 2027-03-06 - Atlanta United/
```

### Directory Naming

Directory names are generated using available match information.

| Match information | Example directory name |
|---|---|
| Date only | `2027-03-06 - Atlanta United` |
| Opponent, unknown venue | `2027-03-06 - Atlanta United vs Orlando City` |
| Home match | `2027-03-06 - Orlando City at Atlanta United` |
| Away match | `2027-03-06 - Atlanta United at Orlando City` |
| Completed match | `2027-03-06 - Orlando City at Atlanta United, W 2-1` |
| Playoff match | `2027-03-06 - Orlando City at Atlanta United, W 2-1, MLS Cup Playoffs` |
| Penalty shootout | `2027-03-06 - Orlando City at Atlanta United, D 2-2 W (5-4) pens, MLS Cup Playoffs` |

Scores always place the configured team's goals first, regardless of the match result.

Regular-season designations are omitted from directory names.

### Updating Existing Directories

When additional match information becomes available, Match Library Manager updates the corresponding directory name.

For example:

```text
Before:
2027-03-06 - Atlanta United

After:
2027-03-06 - Orlando City at Atlanta United, W 2-1
```

Existing files and subdirectories are preserved during renaming.

The application uses match dates and team names to identify existing directories. When it cannot confidently identify a match, it reports a conflict rather than arbitrarily renaming a directory.

## CSV Requirements

Each enabled team uses one CSV file.

The minimum information required to process a match is:

- A valid `Date` field in `YYYY-MM-DD` format
- A team identified by its TOML configuration

Other match information, including opponent, venue, result, score, competition, round, and penalty shootout details, is optional.

The application supports CSV comments beginning with `#` and reports invalid dates as warnings.

## Testing

The project includes a dedicated `TEST` team configuration and a sample CSV for testing directory operations without affecting actual match libraries.

Set the test team to `Enabled = true`, disable other teams, and configure `Dry_Run` as appropriate.

Automated tests can also be executed with:

```cmd
python Run_Tests.py
```

These cover directory naming, creation, renaming, dry-run behavior, file preservation, and conflict handling.

## Project Structure

```text
Match_Library_Manager/
├── Core/
│   ├── __init__.py
│   ├── Config.py
│   ├── Directory_Naming.py
│   ├── Library_Management.py
│   └── Match_Processing.py
│
├── Tests/
│   ├── __init__.py
│   ├── Tests_Matchlogs.csv
│   ├── test_directory_naming.py
│   └── test_library_management.py
│
├── Match_Library_Manager.py
├── Run_Tests.py
├── Config.example.toml
├── Config.toml
├── requirements.txt
├── README.md
└── .gitignore
```

`Config.toml`, virtual environments, and generated Python files are excluded from version control.