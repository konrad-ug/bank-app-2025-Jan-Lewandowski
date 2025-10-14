from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        account.balance = 100.0
        assert account.balance == 100.0
        account.balance += 100.0
        assert account.balance == 200.0
        assert account.pesel == "Invalid"

    def test_account_pesel_too_short(self):
        account = Account("John", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_account_pesel_too_short(self):
        account = Account("John", "Doe", "123123123123123213")
        assert account.pesel == "Invalid"

    def test_account_pesel_good(self):
        account = Account("John", "Doe", "12312312312")
        assert account.pesel == "12312312312"

    def test_account_pesel_non_numeric(self):
        account = Account("John", "Doe", "123123abcd")
        assert account.pesel == "Invalid"

    def test_account_promo_valid(self):
        account = Account("John", "Doe", "12312312312", "PROM_abc")
        assert account.balance == 50.0

    def test_account_promo_wrong_prefix(self):
        account = Account("John", "Doe", "PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long(self):
        account = Account("John", "Doe", "PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_wrong_format(self):
        account = Account("John", "Doe", "INVALID_FORMAT")
        assert account.balance == 0.0 

    def test_account_promo_suffix_too_short(self):
        account = Account("John", "Doe", "PROM_a")
        assert account.balance == 0.0