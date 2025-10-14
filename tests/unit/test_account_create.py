from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", 100)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 100
