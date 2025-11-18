from src.company_account import CompanyAccount


class TestCompanyAccount:

    # NIP validation
    def test_company_account_valid_nip_value(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.nip == "1231231231"

    def test_company_account_wrong_nip_value(self):
        company_account = CompanyAccount("firma", "1231213213231231abc")
        assert company_account.nip == "Niepoprawny NIP!"

    def test_company_account_nip_too_short(self):
        company_account = CompanyAccount("firma", "12345")
        assert company_account.nip == "Niepoprawny NIP!"

    def test_company_account_nip_too_long(self):
        company_account = CompanyAccount("firma", "1234567890123")
        assert company_account.nip == "Niepoprawny NIP!"

    def test_company_account_nip_with_letters(self):
        company_account = CompanyAccount("firma", "12345abcde")
        assert company_account.nip == "Niepoprawny NIP!"

    def test_company_account_valid_nip_exactly_10_digits(self):
        company_account = CompanyAccount("firma", "0000000001")
        assert company_account.nip == "0000000001"

    # initialization
    def test_company_account_inherits_from_account(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert hasattr(company_account, "historia")
        assert hasattr(company_account, "balance")

    def test_company_account_initial_balance_is_zero(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.balance == 0.0

    def test_company_account_has_express_fee_defined(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.oplata_za_express_przelew == 5.0

    # get() method
    def test_get_returns_positive_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        result = company_account.get(50.0)
        assert result == 50.0

    def test_get_increases_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.get(50.0)
        assert company_account.balance == 50.0

    def test_get_adds_to_transfer_history(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.get(50.0)
        assert company_account.historia == [50.0]

    def test_get_negative_amount_returns_previous_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        result = company_account.get(-50.0)
        assert result == 0.0

    def test_get_negative_amount_does_not_change_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.get(-50.0)
        assert company_account.balance == 0.0

    # send() method
    def test_send_enough_money_decreases_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.send(30.0)
        assert company_account.balance == 20.0

    def test_send_enough_money_adds_history(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.send(30.0)
        assert company_account.historia == [-30.0]

    def test_send_not_enough_money_returns_same_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 10.0
        result = company_account.send(30.0)
        assert result == 10.0

    def test_send_negative_amount_does_not_change_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 30.0
        company_account.send(-20.0)
        assert company_account.balance == 30.0

    # express_send method
    def test_express_send_enough_money_decreases_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.express_send(30.0)
        assert company_account.balance == 15.0

    def test_express_send_enough_money_adds_history(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.express_send(30.0)
        assert company_account.historia == [-35.0]

    def test_express_send_not_enough_money_returns_message(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 0.0
        result = company_account.express_send(30.0)
        assert result == "Not enough money"

    def test_express_send_negative_amount_does_not_change_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 30.0
        company_account.express_send(-20.0)
        assert company_account.balance == 30.0

    def test_express_send_does_not_allow_negative_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 5.0
        company_account.express_send(6.0)
        assert company_account.balance == 5.0

    def test_express_send_allows_minimum_negative_equal_to_fee(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 5.0
        result = company_account.express_send(5.0)
        assert result == -5.0
        assert company_account.balance == -5.0
        assert company_account.historia == [-10.0]

    # is_express_send_correct()
    def test_is_express_send_correct_true(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 100.0
        assert company_account.is_express_send_correct(50.0)

    def test_is_express_send_correct_false_negative_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 100.0
        assert not company_account.is_express_send_correct(-10.0)

    def test_is_express_send_correct_false_not_enough_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 20.0
        assert not company_account.is_express_send_correct(50.0)

    def test_get_zero_amount_no_change(self):
        company_account = CompanyAccount("firma", "1231231231")
        result = company_account.get(0.0)
        assert result == 0.0
        assert company_account.balance == 0.0
        assert company_account.historia == []

    def test_send_exact_balance_zeroes_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.send(50.0)
        assert company_account.balance == 0.0
        assert company_account.historia == [-50.0]

    def test_express_send_zero_amount_returns_message(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 10.0
        result = company_account.express_send(0.0)
        assert result == "Not enough money"
        assert company_account.balance == 10.0
        assert company_account.historia == []

    def test_is_express_send_correct_zero_amount_false(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 100.0
        assert not company_account.is_express_send_correct(0.0)
