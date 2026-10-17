"""Core logic for a single rotating susu group. Money is stored as integer pesewas."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

class SusuError(Exception): pass
class MoneyError(SusuError): pass
class MemberError(SusuError): pass
class WeekError(SusuError): pass

def parse_ghs_to_pesewas(amount):
    try:
        value = Decimal(str(amount).strip())
    except (InvalidOperation, ValueError, AttributeError):
        raise MoneyError("Enter a valid amount, e.g. 50.00.") from None
    if not value.is_finite() or value <= 0:
        raise MoneyError("Amount must be a finite number greater than zero.")
    if value.as_tuple().exponent < -2:
        raise MoneyError("Use no more than two decimal places.")
    pesewas = value * 100
    if pesewas != pesewas.to_integral_value():
        raise MoneyError("Amount cannot be represented exactly in pesewas.")
    return int(pesewas)

def format_ghs(pesewas):
    return f"GHS {pesewas // 100}.{pesewas % 100:02d}"

@dataclass(frozen=True)
class Member:
    name: str
    key: str

@dataclass(frozen=True)
class Payout:
    week: int
    recipient: str
    amount_pesewas: int

class SusuGroup:
    def __init__(self, weekly_contribution):
        self.weekly_contribution_pesewas = parse_ghs_to_pesewas(weekly_contribution)
        self.members = []
        self._member_by_key = {}
        self._payments = {1: {}}
        self.payout_history = []
        self.current_week = 1
        self._membership_frozen = False
        self._complete = False

    @property
    def pot_pesewas(self):
        return self.weekly_contribution_pesewas * len(self.members)

    @property
    def is_complete(self):
        return self._complete

    def add_member(self, name):
        if self._membership_frozen:
            raise MemberError("Membership is locked after the first contribution.")
        if not isinstance(name, str) or not name.strip():
            raise MemberError("Member name or ID cannot be empty.")
        display = name.strip()
        key = display.casefold()
        if key in self._member_by_key:
            raise MemberError(f"Member '{display}' already exists.")
        member = Member(display, key)
        self.members.append(member)
        self._member_by_key[key] = member
        return member

    def _get_member(self, name):
        if not isinstance(name, str):
            raise MemberError("Provide a valid member name or ID.")
        member = self._member_by_key.get(name.strip().casefold())
        if member is None:
            raise MemberError(f"Unknown member: '{name}'.")
        return member

    def amount_paid(self, member_name, week=None):
        member = self._get_member(member_name)
        week = self.current_week if week is None else week
        return self._payments.get(week, {}).get(member.key, 0)

    def amount_owed(self, member_name, week=None):
        return self.weekly_contribution_pesewas - self.amount_paid(member_name, week)

    def record_contribution(self, member_name, amount):
        if self._complete:
            raise WeekError("The susu rotation is complete.")
        member = self._get_member(member_name)
        amount_pesewas = parse_ghs_to_pesewas(amount)
        payments = self._payments.setdefault(self.current_week, {})
        already = payments.get(member.key, 0)
        owed = self.weekly_contribution_pesewas - already
        if amount_pesewas > owed:
            raise MoneyError(f"Payment exceeds amount owed. {member.name} owes {format_ghs(owed)}.")
        self._membership_frozen = True
        payments[member.key] = already + amount_pesewas
        return payments[member.key]

    def close_week(self):
        if self._complete:
            raise WeekError("The susu rotation is already complete.")
        if not self.members:
            raise WeekError("Add at least one member before closing a week.")
        report = self.get_report()
        if report["members_owing"]:
            return {"closed": False, "week": self.current_week,
                    "members_owing": report["members_owing"],
                    "message": "Week remains open because some members have outstanding balances."}
        recipient = self.members[len(self.payout_history)]
        payout = Payout(self.current_week, recipient.name, self.pot_pesewas)
        self.payout_history.append(payout)
        if len(self.payout_history) >= len(self.members):
            self._complete = True
        else:
            self.current_week += 1
            self._payments[self.current_week] = {}
        return {"closed": True, "week": payout.week, "recipient": payout.recipient,
                "amount_pesewas": payout.amount_pesewas, "rotation_complete": self._complete,
                "message": f"{payout.recipient} receives {format_ghs(payout.amount_pesewas)}."}

    def get_report(self):
        payments = self._payments.get(self.current_week, {})
        paid, owing = [], []
        for member in self.members:
            amount = payments.get(member.key, 0)
            owed = self.weekly_contribution_pesewas - amount
            if owed == 0:
                paid.append(member.name)
            else:
                owing.append({"member": member.name, "paid_pesewas": amount, "owes_pesewas": owed})
        return {"current_week": self.current_week,
                "weekly_contribution_pesewas": self.weekly_contribution_pesewas,
                "pot_pesewas": self.pot_pesewas, "paid_in_full": paid,
                "members_owing": owing,
                "payout_history": [{"week": p.week, "recipient": p.recipient,
                                    "amount_pesewas": p.amount_pesewas} for p in self.payout_history],
                "rotation_complete": self._complete}
