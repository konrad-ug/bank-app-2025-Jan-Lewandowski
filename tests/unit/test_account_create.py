from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12312321312")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        account.balance = 100
        assert account.balance == 100
        account.balance += 100
        assert account.balance == 200
        assert account.pesel == "12312321312"
