import json

import pytest
import requests

from src import company_account as company_account_module
from src.company_account import CompanyAccount

@pytest.fixture(autouse=True)
def mock_mf_api(mocker):
    state = {"status": "Czynny", "status_code": 200, "subject": True, "call_count": 0, "last_url": None}

    def fake_get(url, timeout=10):
        state["call_count"] += 1
        state["last_url"] = url

        resp = mocker.Mock()
        resp.status_code = state["status_code"]

        def resp_json():
            subject = {"statusVat": state["status"]} if state.get("subject") else None
            return {"result": {"subject": subject}}

        resp.json.side_effect = resp_json
        resp.text = json.dumps(resp_json())

        def raise_for_status():
            if resp.status_code >= 400:
                raise requests.HTTPError(f"{resp.status_code}")

        resp.raise_for_status.side_effect = raise_for_status
        return resp

    mocker.patch.object(company_account_module.requests, "get", side_effect=fake_get)
    return state

class TestCompanyAccount:
    @pytest.fixture
    def company_account(self):
        company_account = CompanyAccount("firma", "1231231231")
        return company_account
    
    @pytest.mark.parametrize("historia, amount, expected_result, expected_balance", [
        ([100, 100, 100, -1775, 3000], 600, True, 2125),
        ([-100, 100, -1775, 100, 1700], 700, False, 25),
        ([-100, 20000, -100, 100, -1000], 1000, False, 18900),
        ([], 100, False, 0),
    ])
    def test_take_loan(self, company_account: CompanyAccount, historia, amount, expected_result, expected_balance):
      company_account.historia = historia
      company_account.balance = 0
      result = company_account.take_loan(amount)
      assert result == expected_result
      assert company_account.balance == expected_balance

    # NIP validation
    def test_company_account_valid_nip_value(self, company_account: CompanyAccount):
        assert company_account.nip == "1231231231"

    def test_check_vat_status_returns_true_for_czynny(self):
        account = CompanyAccount("firma", "1234567890")
        assert account.check_vat_status("1234567890") is True

    def test_check_vat_status_returns_false_for_non_czynny(self, mock_mf_api):
        mock_mf_api["status"] = "Zwolniony"
        account = CompanyAccount("firma", "1234567890")
        assert account.check_vat_status("1234567890") is False

    def test_check_vat_status_raises_for_404(self, mock_mf_api):
        mock_mf_api["status_code"] = 404
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("firma", "1234567890")

    def test_check_vat_status_raises_when_subject_missing(self, mock_mf_api):
        mock_mf_api["subject"] = False
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("firma", "1234567890")

    def test_constructor_raises_when_api_returns_404(self, mock_mf_api):
        mock_mf_api["status_code"] = 404
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("firma", "1234567890")

    def test_company_account_wrong_nip_value(self):
        company_account = CompanyAccount("firma", "1231213213231231abc")
        assert company_account.nip == "Niepoprawny NIP!"

    def test_company_account_nip_too_short(self):
        company_account = CompanyAccount("firma", "12345")
        assert company_account.nip == "Niepoprawny NIP!"
        # no remote call for invalid length
        assert company_account.is_vat_active is None

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
    def test_company_account_inherits_from_account(self, company_account: CompanyAccount):
        assert hasattr(company_account, "historia")
        assert hasattr(company_account, "balance")

    def test_company_account_initial_balance_is_zero(self, company_account: CompanyAccount):
        assert company_account.balance == 0.0

    def test_company_account_has_express_fee_defined(self, company_account: CompanyAccount):
        assert company_account.oplata_za_express_przelew == 5.0

    # get() method
    def test_get_returns_positive_amount(self, company_account: CompanyAccount):
        result = company_account.get(50.0)
        assert result == 50.0

    def test_get_increases_balance(self, company_account: CompanyAccount):
        company_account.get(50.0)
        assert company_account.balance == 50.0

    def test_get_adds_to_transfer_history(self, company_account: CompanyAccount):
        company_account.get(50.0)
        assert company_account.historia == [50.0]

    def test_get_negative_amount_returns_previous_balance(self, company_account: CompanyAccount):
        result = company_account.get(-50.0)
        assert result == 0.0

    def test_get_negative_amount_does_not_change_balance(self, company_account: CompanyAccount):
        company_account.get(-50.0)
        assert company_account.balance == 0.0

    # send() method
    def test_send_enough_money_decreases_balance(self, company_account: CompanyAccount):
        company_account.balance = 50.0
        company_account.send(30.0)
        assert company_account.balance == 20.0

    def test_send_enough_money_adds_history(self, company_account: CompanyAccount):
        company_account.balance = 50.0
        company_account.send(30.0)
        assert company_account.historia == [-30.0]

    def test_send_not_enough_money_returns_same_balance(self, company_account: CompanyAccount):
        company_account.balance = 10.0
        result = company_account.send(30.0)
        assert result == 10.0

    def test_send_negative_amount_does_not_change_balance(self, company_account: CompanyAccount):
        company_account.balance = 30.0
        company_account.send(-20.0)
        assert company_account.balance == 30.0

    # express_send method
    def test_express_send_enough_money_decreases_balance(self, company_account: CompanyAccount):
        company_account.balance = 50.0
        company_account.express_send(30.0)
        assert company_account.balance == 15.0

    def test_express_send_enough_money_adds_history(self, company_account: CompanyAccount):
        company_account.balance = 50.0
        company_account.express_send(30.0)
        assert company_account.historia == [-35.0]

    def test_express_send_not_enough_money_returns_message(self, company_account: CompanyAccount):
        company_account.balance = 0.0
        result = company_account.express_send(30.0)
        assert result == "Not enough money"

    def test_express_send_negative_amount_does_not_change_balance(self, company_account: CompanyAccount):
        company_account.balance = 30.0
        company_account.express_send(-20.0)
        assert company_account.balance == 30.0

    def test_express_send_does_not_allow_negative_balance(self, company_account: CompanyAccount):
        company_account.balance = 5.0
        company_account.express_send(6.0)
        assert company_account.balance == 5.0

    def test_express_send_allows_minimum_negative_equal_to_fee(self, company_account: CompanyAccount):
        company_account.balance = 5.0
        result = company_account.express_send(5.0)
        assert result == -5.0
        assert company_account.balance == -5.0
        assert company_account.historia == [-10.0]
        
    def test_is_express_send_correct_true(self, company_account: CompanyAccount):
        company_account.balance = 100.0
        assert company_account.is_express_send_correct(50.0)

    def test_is_express_send_correct_false_negative_amount(self, company_account: CompanyAccount):
        
        company_account.balance = 100.0
        assert not company_account.is_express_send_correct(-10.0)

    def test_is_express_send_correct_false_not_enough_balance(self, company_account: CompanyAccount):
        company_account.balance = 20.0
        assert not company_account.is_express_send_correct(50.0)

    def test_get_zero_amount_no_change(self, company_account: CompanyAccount):
        result = company_account.get(0.0)
        assert result == 0.0
        assert company_account.balance == 0.0
        assert company_account.historia == []

    def test_send_exact_balance_zeroes_balance(self, company_account: CompanyAccount):
        company_account.balance = 50.0
        company_account.send(50.0)
        assert company_account.balance == 0.0
        assert company_account.historia == [-50.0]

    def test_express_send_zero_amount_returns_message(self, company_account: CompanyAccount):
        company_account.balance = 10.0
        result = company_account.express_send(0.0)
        assert result == "Not enough money"
        assert company_account.balance == 10.0
        assert company_account.historia == []

    def test_is_express_send_correct_zero_amount_false(self, company_account: CompanyAccount):
        company_account.balance = 100.0
        assert not company_account.is_express_send_correct(0.0)