from src.personal_account import PersonalAccount
import pytest

class TestPersonalAccount:
    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "12312312312")
        return account
    
    @pytest.mark.parametrize("historia, amount, expected_result, expected_balance", [
        ([100, 100, 100], 500, True, 500),
        ([-100, 100, -100, 100, 1000], 700, True, 700),
        ([-100, 20000, -100, 100, -1000], 1000, True, 1000),
        ([100], 666, False, 0),
        ([-100, 100, 100, 100, -6000, 200], 500, False, 0),
    ])
    def test_loan(self, account: PersonalAccount, historia, amount, expected_result, expected_balance):
      account.historia = historia
      account.balance = 0
      result = account.submit_for_loan(amount)
      assert result == expected_result
      assert account.balance == expected_balance

    # Account creation and PESEL validation – używamy fixture gdzie się da
    def test_account_creation_first_name(self, account: PersonalAccount):
        assert account.first_name == "John"

    def test_account_creation_last_name(self, account: PersonalAccount):
        assert account.last_name == "Doe"

    def test_account_creation_invalid_pesel(self):
        account = PersonalAccount("John", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_account_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_account_pesel_too_long(self):
        account = PersonalAccount("John", "Doe", "123123123123123213")
        assert account.pesel == "Invalid"

    def test_account_pesel_valid(self, account: PersonalAccount):
        assert account.pesel == "12312312312"

    def test_account_pesel_non_numeric(self):
        account = PersonalAccount("John", "Doe", "123123abcd")
        assert account.pesel == "Invalid"

    # Promo code tests – nie da się użyć fixture (bo promo wpływa na konstruktor)
    def test_account_promo_valid(self):
        account = PersonalAccount("John", "Doe", "12312312312", "PROM_abc")
        assert account.balance == 50.0

    def test_account_promo_wrong_prefix(self):
        account = PersonalAccount("John", "Doe", "12312312312", "PRO_abc")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long(self):
        account = PersonalAccount("John", "Doe", "12312312312", "PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_short(self):
        account = PersonalAccount("John", "Doe", "12312312312", "PROM_a")
        assert account.balance == 0.0

    def test_account_promo_wrong_format(self):
        account = PersonalAccount("John", "Doe", "12312312312", "INVALID_FORMAT")
        assert account.balance == 0.0

    # get() method – używamy fixture
    def test_account_get_positive_amount_returns_value(self, account: PersonalAccount):
        result = account.get(50.0)
        assert result == 50.0

    def test_account_get_positive_amount_increases_balance(self, account: PersonalAccount):
        account.get(50.0)
        assert account.balance == 50.0

    def test_account_get_positive_amount_adds_to_history(self, account: PersonalAccount):
        account.get(50.0)
        assert account.historia == [50.0]

    def test_account_get_negative_amount_returns_zero(self, account: PersonalAccount):
        result = account.get(-50.0)
        assert result == 0.0

    def test_account_get_negative_amount_does_not_change_balance(self, account: PersonalAccount):
        account.get(-50.0)
        assert account.balance == 0.0

    def test_account_get_negative_amount_not_added_to_history(self, account: PersonalAccount):
        account.get(-50.0)
        assert account.historia == []

    # send() method – fixture + ręczne ustawienie balance gdzie potrzebne
    def test_account_send_enough_money_decreases_balance(self, account: PersonalAccount):
        account.balance = 50.0
        account.historia = []
        account.send(30.0)
        assert account.balance == 20.0

    def test_account_send_enough_money_adds_to_history(self, account: PersonalAccount):
        account.balance = 50.0
        account.historia = []
        account.send(30.0)
        assert account.historia == [-30.0]

    def test_account_send_not_enough_money_returns_zero(self, account: PersonalAccount):
        account.balance = 0.0
        result = account.send(30.0)
        assert result == 0.0

    def test_account_send_negative_amount_does_not_change_balance(self, account: PersonalAccount):
        account.balance = 30.0
        account.send(-20.0)
        assert account.balance == 30.0

    def test_account_send_negative_amount_not_added_to_history(self, account: PersonalAccount):
        account.balance = 30.0
        account.historia = []
        account.send(-20.0)
        assert account.historia == []

    # express_send() method
    def test_account_express_send_enough_money_decreases_balance(self, account: PersonalAccount):
        account.balance = 50.0
        account.historia = []
        account.express_send(30.0)
        assert account.balance == 19.0

    def test_account_express_send_enough_money_adds_to_history(self, account: PersonalAccount):
        account.balance = 50.0
        account.historia = []
        account.express_send(30.0)
        assert account.historia == [-31.0]

    def test_account_express_send_not_enough_money_returns_message(self, account: PersonalAccount):
        account.balance = 0.0
        result = account.express_send(30.0)
        assert result == "Not enough money"

    def test_account_express_send_negative_amount_does_not_change_balance(self, account: PersonalAccount):
        account.balance = 30.0
        account.express_send(-20.0)
        assert account.balance == 30.0

    def test_account_express_send_negative_amount_not_added_to_history(self, account: PersonalAccount):
        account.balance = 30.0
        account.historia = []
        account.express_send(-20.0)
        assert account.historia == []

    def test_account_express_send_negative_balance_not_allowed(self, account: PersonalAccount):
        account.balance = 5.0
        account.historia = []
        account.express_send(5.0)
        assert account.balance == -1.0

    def test_account_express_send_negative_balance_recorded_in_history(self, account: PersonalAccount):
        account.balance = 5.0
        account.historia = []
        account.express_send(5.0)
        assert account.historia == [-6.0]

    def test_get_zero_amount_no_change(self, account: PersonalAccount):
        result = account.get(0.0)
        assert result == 0.0
        assert account.balance == 0.0
        assert account.historia == []

    def test_send_exact_balance_zeroes_balance(self, account: PersonalAccount):
        account.balance = 40.0
        account.historia = []
        account.send(40.0)
        assert account.balance == 0.0
        assert account.historia == [-40.0]

    def test_express_send_zero_amount_returns_message(self, account: PersonalAccount):
        account.balance = 10.0
        result = account.express_send(0.0)
        assert result == "Not enough money"
        assert account.balance == 10.0
        assert account.historia == []

    def test_is_express_send_correct_zero_amount_false(self, account: PersonalAccount):
        account.balance = 100.0
        assert not account.is_express_send_correct(0.0)

    def test_is_promo_code_valid_direct_calls(self, account: PersonalAccount):
        assert account.is_promo_code_valid(None) is False
        assert account.is_promo_code_valid("PROM_abc") is True
        assert account.is_promo_code_valid("PROM_a") is None

    def test_is_not_pensioner_month_over_20_true(self):
        account = PersonalAccount("John", "Doe", "33501234567")
        assert account.is_not_pensioner("33501234567") is True

    def test_is_not_pensioner_rok_ge_60_true(self):
        account = PersonalAccount("John", "Doe", "60001234567")
        assert account.is_not_pensioner("60001234567") is True

    def test_is_not_pensioner_false_when_younger(self, account: PersonalAccount):
        assert account.is_not_pensioner("55123456789") is False