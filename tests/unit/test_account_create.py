from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        account.balance = 100
        assert account.balance == 100
        account.balance += 100
        assert account.balance == 200
        assert account.pesel == "Invalid"

    def test_account_creation_pesel_too_short(self):
        account = Account("John", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_account_creation_pesel_too_short(self):
        account = Account("John", "Doe", "123123123123123213")
        assert account.pesel == "Invalid"

    def test_account_creation_pesel_good(self):
        account = Account("John", "Doe", "12312312312")
        assert account.pesel == "12312312312"

    def test_account_creation_pesel_non_numeric(self):
        account = Account("John", "Doe", "123123abcd")
        assert account.pesel == "Invalid"