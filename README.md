# Susu Group Tracker
A Python command-line app for one rotating savings group.

## Requirements
Python 3.10+; no third-party packages.

## Run
```bash
python main.py
```
Follow the menu to add members, record payments, close weeks, and view reports.

## Test
```bash
python -m unittest discover -s tests -v
```

## Money
Amounts are converted to integer pesewas (100 pesewas = GHS 1.00), avoiding floating-point rounding errors. Inputs may have up to two decimal places.

## Structure
- `main.py`: interactive CLI
- `susu/tracker.py`: business logic
- `tests/test_tracker.py`: automated tests
- `NOTES.md`: assumptions and future improvements
