# Susu Group Tracker

A Python command-line application for managing a rotating savings group (Susu). Members contribute a fixed amount each week, and the entire pot is paid to one member in the order they joined.

## Features

- Register group members with unique names or IDs.
- Record fixed weekly contributions and partial payments.
- Validate payments and reject unknown members, duplicate names, zero or negative amounts, and overpayments.
- Prevent a week from closing while members have outstanding balances.
- Distribute the full pot to the next member in the payout order.
- Track the current week, payment balances, and payout history.
- Handle money using integer pesewas to avoid floating-point rounding errors.

## Requirements

- Python 3.10 or later.
- No third-party packages required.

## Run the Application

On Windows, open PowerShell in the project directory and run:

```powershell
py main.py
```

Follow the interactive menu to manage members, record contributions, close weeks, and view reports.

## Run the Tests

```powershell
py -m unittest discover -s tests -v
```

The automated tests cover payment validation, partial contributions, outstanding balances, membership rules, and payout rotation.

## Money Handling

Amounts are converted to integer pesewas (100 pesewas = GHS 1.00) to avoid floating-point rounding errors. Input amounts may contain up to two decimal places.

## Project Structure

```text
susu_group_tracker/
├── main.py
├── susu/
│   ├── __init__.py
│   └── tracker.py
├── tests/
│   └── test_tracker.py
├── examples/
│   └── sample_scenario.md
├── README.md
├── NOTES.md
└── .gitignore
```

## Design Assumptions

See [NOTES.md](NOTES.md) for the project's assumptions, design decisions, known limitations, and potential future improvements.

## Purpose

This project demonstrates Python programming, financial validation, separation of business logic from the command-line interface, automated testing, and version control through Git.
