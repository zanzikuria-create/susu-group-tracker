# Manual Acceptance Scenario

Use this scenario to manually verify the example from the challenge.

1. Start `python main.py` and set the weekly contribution to `50.00`.
2. Add members `Ama`, `Kofi`, and `Esi`, then finish adding members with a blank name.
3. Record `50.00` for Ama, `50.00` for Kofi, and `30.00` for Esi.
4. Choose **Close current week**. The week must remain open, and Esi must be reported as owing `GHS 20.00`; no payout should be recorded.
5. Record another `20.00` for Esi.
6. Close the week again. Ama should receive `GHS 150.00`, and week 2 should begin.
7. Show the report and confirm Ama appears in the payout history.
