from susu import SusuGroup, SusuError, format_ghs

def show_report(group):
    r = group.get_report()
    print("\n=== SUSU GROUP REPORT ===")
    print(f"Current week: {r['current_week']}")
    print(f"Weekly contribution: {format_ghs(r['weekly_contribution_pesewas'])}")
    print(f"Pot: {format_ghs(r['pot_pesewas'])}")
    print("Paid in full:", ", ".join(r["paid_in_full"]) or "None")
    print("Members owing:")
    for item in r["members_owing"]:
        print(f"  - {item['member']}: paid {format_ghs(item['paid_pesewas'])}, owes {format_ghs(item['owes_pesewas'])}")
    if not r["members_owing"]: print("  None")
    print("Payout history:")
    for p in r["payout_history"]:
        print(f"  - Week {p['week']}: {p['recipient']} received {format_ghs(p['amount_pesewas'])}")
    if not r["payout_history"]: print("  No payouts yet")
    if r["rotation_complete"]: print("Rotation status: COMPLETE")

def main():
    print("Susu Group Tracker")
    while True:
        try:
            group = SusuGroup(input("Fixed weekly contribution in GHS (e.g. 50.00): "))
            break
        except SusuError as e: print("Error:", e)
    print("Add members; enter a blank name when finished.")
    while True:
        name = input("Member name/ID: ")
        if not name.strip(): break
        try:
            group.add_member(name); print(f"Added {name.strip()}.")
        except SusuError as e: print("Error:", e)
    while True:
        print("\n1 Add member\n2 Record contribution\n3 Close current week\n4 Show report\n5 Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                name = input("Member name/ID: "); group.add_member(name); print("Member added.")
            elif choice == "2":
                name = input("Member name/ID: "); amount = input("Amount in GHS: ")
                total = group.record_contribution(name, amount)
                print("Payment recorded. Total paid this week:", format_ghs(total))
            elif choice == "3":
                result = group.close_week(); print(result["message"])
                for item in result.get("members_owing", []):
                    print(f"  - {item['member']} owes {format_ghs(item['owes_pesewas'])}")
            elif choice == "4": show_report(group)
            elif choice == "5": print("Goodbye."); return
            else: print("Choose an option from 1 to 5.")
        except SusuError as e: print("Error:", e)

if __name__ == "__main__": main()
