# Assumptions and Decisions

1. **Currency:** Contributions are recorded in Ghanaian cedis (GHS), with a maximum of two decimal places. Money is stored as integer pesewas (100 pesewas = GHS 1.00) to avoid floating-point rounding errors.

2. **Member uniqueness:** Member names or IDs must be unique after trimming surrounding whitespace and ignoring letter case.

3. **Membership changes:** Members can only be added before the first contribution is recorded. This preserves the agreed contribution amount, pot calculation, and payout order.

4. **Fixed contributions:** Every member owes the same fixed contribution amount each week.

5. **Partial payments:** Members may pay in installments. A payment cannot exceed the member's outstanding balance for the current week.

6. **Week closure:** A week can only close when every member has paid their full contribution. If any balance remains outstanding, the week stays open, no payout occurs, and the remaining amounts can be reported.

7. **Pot calculation:** The weekly pot is calculated as the fixed weekly contribution multiplied by the total number of members.

8. **Payout order:** Each member receives the pot once per rotation, following the order in which they joined the group.

9. **Empty groups:** A week cannot close when the group has no members.

10. **Data storage:** Data is held in memory only. Exiting the application resets the group's members, payments, and payout history.

## Improvements with More Time

- Add SQLite or PostgreSQL persistence so group data survives application restarts.
- Introduce a transaction and audit log, with CSV export for record-keeping.
- Support multiple groups, authentication, and more robust member identifiers.
- Add continuous integration (CI) and additional edge-case tests.
- Confirm with users whether the payout rotation should restart after every member has received a payout and how late membership should be handled.

## Scope

This version focuses on the core rules of one rotating savings group through a command-line interface. Persistent storage, multiple groups, and authentication are outside the current scope.
