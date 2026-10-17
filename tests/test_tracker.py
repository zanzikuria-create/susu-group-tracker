import unittest
from susu import SusuGroup, MoneyError, MemberError, WeekError
from susu.tracker import parse_ghs_to_pesewas, format_ghs

class SusuGroupTests(unittest.TestCase):
    def setUp(self):
        self.group = SusuGroup("50.00")
        for name in ("Ama", "Kofi", "Esi"): self.group.add_member(name)

    def test_partial_payment_balance(self):
        self.group.record_contribution("Esi", "30.00")
        self.assertEqual(self.group.amount_paid("Esi"), 3000)
        self.assertEqual(self.group.amount_owed("Esi"), 2000)

    def test_week_cannot_close_if_member_owes(self):
        self.group.record_contribution("Ama", "50")
        self.group.record_contribution("Kofi", "50")
        self.group.record_contribution("Esi", "30")
        result = self.group.close_week()
        self.assertFalse(result["closed"])
        self.assertEqual(result["members_owing"][0]["owes_pesewas"], 2000)
        self.assertEqual(len(self.group.payout_history), 0)
        self.assertEqual(self.group.current_week, 1)

    def test_full_week_pays_first_member_and_advances(self):
        for n in ("Ama", "Kofi", "Esi"): self.group.record_contribution(n, "50")
        result = self.group.close_week()
        self.assertEqual(result["recipient"], "Ama")
        self.assertEqual(result["amount_pesewas"], 15000)
        self.assertEqual(self.group.current_week, 2)

    def test_partial_installments_can_complete_payment(self):
        self.group.record_contribution("Esi", "30")
        self.group.record_contribution("Esi", "20")
        self.assertEqual(self.group.amount_owed("Esi"), 0)
        self.assertIn("Esi", self.group.get_report()["paid_in_full"])

    def test_rejects_zero_and_negative(self):
        for amount in ("0", "-1"):
            with self.subTest(amount=amount), self.assertRaises(MoneyError):
                self.group.record_contribution("Ama", amount)

    def test_rejects_overpayment(self):
        self.group.record_contribution("Ama", "40")
        with self.assertRaises(MoneyError): self.group.record_contribution("Ama", "10.01")

    def test_rejects_unknown_member(self):
        with self.assertRaises(MemberError): self.group.record_contribution("Yaw", "10")

    def test_rejects_duplicate_member_case_insensitive(self):
        with self.assertRaises(MemberError): self.group.add_member(" ama ")

    def test_exact_money_and_decimal_validation(self):
        self.assertEqual(parse_ghs_to_pesewas("12.30"), 1230)
        self.assertEqual(format_ghs(1230), "GHS 12.30")
        with self.assertRaises(MoneyError): parse_ghs_to_pesewas("1.001")

    def test_membership_freezes_after_first_payment(self):
        self.group.record_contribution("Ama", "1")
        with self.assertRaises(MemberError): self.group.add_member("Yaw")

    def test_payout_order_and_rotation_completion(self):
        for n in ("Ama", "Kofi", "Esi"): self.group.record_contribution(n, "50")
        self.group.close_week()
        for n in ("Ama", "Kofi", "Esi"): self.group.record_contribution(n, "50")
        self.assertEqual(self.group.close_week()["recipient"], "Kofi")
        for n in ("Ama", "Kofi", "Esi"): self.group.record_contribution(n, "50")
        result = self.group.close_week()
        self.assertEqual(result["recipient"], "Esi")
        self.assertTrue(result["rotation_complete"])
        with self.assertRaises(WeekError): self.group.close_week()
        with self.assertRaises(WeekError): self.group.record_contribution("Ama", "1")

    def test_empty_group_cannot_close(self):
        with self.assertRaises(WeekError): SusuGroup("50").close_week()

if __name__ == "__main__": unittest.main()
