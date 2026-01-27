from unittest.mock import Mock

import pytest

import app.api as api_module
from src.personal_account import PersonalAccount


@pytest.fixture()
def client():
    api_module.app.config.update
    with api_module.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_registry():
    api_module.registry.accounts.clear()
    yield


def test_save_accounts_calls_repository(client, monkeypatch):
    repo_mock = Mock()
    monkeypatch.setattr(api_module, "MongoAccountsRepository", lambda: repo_mock)

    client.post(
        "/api/accounts",
        json={"first_name": "Anna", "last_name": "Nowak", "pesel": "12345678901"},
    )

    response = client.post("/api/accounts/save")

    assert response.status_code == 200
    repo_mock.save_all.assert_called_once()
    saved_accounts = repo_mock.save_all.call_args[0][0]
    assert len(saved_accounts) == 1
    assert saved_accounts[0].pesel == "12345678901"


def test_load_accounts_populates_registry(client, monkeypatch):
    repo_mock = Mock()
    repo_mock.load_all.return_value = [
        PersonalAccount("A", "B", "11111111111"),
        PersonalAccount("C", "D", "22222222222"),
    ]
    monkeypatch.setattr(api_module, "MongoAccountsRepository", lambda: repo_mock)

    response = client.post("/api/accounts/load")

    assert response.status_code == 200
    assert api_module.registry.get_account_count() == 2
    assert api_module.registry.search_account_based_on_pesel("11111111111") is not None
    assert api_module.registry.search_account_based_on_pesel("22222222222") is not None


def test_clear_accounts_empties_registry(client):
    client.post(
        "/api/accounts",
        json={"first_name": "A", "last_name": "B", "pesel": "33333333333"},
    )
    response = client.post("/api/accounts/clear")

    assert response.status_code == 200
    assert api_module.registry.get_account_count() == 0
