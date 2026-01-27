import json
from datetime import date

import pytest

import src.account as account_module
import src.company_account as company_account_module
from src.company_account import CompanyAccount
from src.personal_account import PersonalAccount


@pytest.fixture
def mock_smtp_send(mocker):
    return mocker.patch.object(account_module.SMTPClient, "send")


@pytest.fixture
def mock_mf_api(mocker):
    response = mocker.Mock()
    response.status_code = 200
    payload = {"result": {"subject": {"statusVat": "Czynny"}}}
    response.json.return_value = payload
    response.text = json.dumps(payload)
    response.raise_for_status = mocker.Mock()

    patched_get = mocker.patch.object(company_account_module.requests, "get", return_value=response)
    return patched_get


def test_send_history_via_email_personal_success(mock_smtp_send):
    mock_smtp_send.return_value = True
    account = PersonalAccount("Jan", "Kowalski", "12345678901")
    account.historia = [100, -20]

    expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
    expected_body = f"Personal account history: {account.historia}"

    result = account.send_history_via_email("user@example.com")

    assert result is True
    mock_smtp_send.assert_called_once_with(
        expected_subject,
        expected_body,
        "user@example.com",
    )


def test_send_history_via_email_personal_failure(mock_smtp_send):
    mock_smtp_send.return_value = False
    account = PersonalAccount("Jan", "Kowalski", "12345678901")
    account.historia = [10]

    expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
    expected_body = f"Personal account history: {account.historia}"

    result = account.send_history_via_email("user@example.com")

    assert result is False
    mock_smtp_send.assert_called_once_with(
        expected_subject,
        expected_body,
        "user@example.com",
    )


def test_send_history_via_email_company_success(mock_smtp_send, mock_mf_api):
    mock_smtp_send.return_value = True
    account = CompanyAccount("ACME", "1234567890")
    account.historia = [200, -50]

    expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
    expected_body = f"Company account history: {account.historia}"

    result = account.send_history_via_email("corp@example.com")

    assert result is True
    mock_smtp_send.assert_called_once_with(
        expected_subject,
        expected_body,
        "corp@example.com",
    )
    assert mock_mf_api.call_count == 1


def test_send_history_via_email_company_failure(mock_smtp_send, mock_mf_api):
    mock_smtp_send.return_value = False
    account = CompanyAccount("ACME", "1234567890")
    account.historia = [-10]

    expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
    expected_body = f"Company account history: {account.historia}"

    result = account.send_history_via_email("corp@example.com")

    assert result is False
    mock_smtp_send.assert_called_once_with(
        expected_subject,
        expected_body,
        "corp@example.com",
    )
    assert mock_mf_api.call_count == 1
