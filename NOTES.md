# Assumptions and Decisions

1. Contributions are in GHS, with at most two decimal places; money is stored as integer pesewas.
2. Member names/IDs are unique after trimming whitespace and ignoring letter case.
3. Members can only be added before the first contribution is recorded, preserving the agreed pot and payout order.
4. Every member owes the same fixed contribution each week.
5. Partial payments are allowed, but a member cannot pay more than their remaining balance.
6. A week closes only when all members have paid in full. Otherwise the week remains open, no payout occurs, and outstanding balances are reported.
7. The pot equals weekly contribution multiplied by the number of members.
8. Each member receives one payout in join order. The rotation is complete after every member has received once.
9. A week cannot close if there are no members.
10. Data is held in memory only; exiting the program resets it.

## Improvements with more time
- Persist data in SQLite/PostgreSQL.
- Add a transaction/audit log and CSV export.
- Support multiple groups, authentication, and stronger member IDs.
- Add CI and more edge-case tests.
- Confirm with users whether a rotation should repeat and whether late membership should be allowed.
