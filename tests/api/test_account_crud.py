# tests/api/test_account_crud.py
import pytest
from app.api import app, registry


@pytest.fixture(autouse=True)
def clean_registry():
    registry.accounts.clear()
    yield


def test_create_account():
    with app.test_client() as client:
        response = client.post("/api/accounts", json={
            "first_name": "James",
            "last_name": "Hetfield",
            "pesel": "89092909825"
        })
        assert response.status_code == 201
        assert response.get_json()["message"] == "Account created"


def test_get_allaccounts_empty_at_start():
    with app.test_client() as client:
        response = client.get("/api/accounts")
        assert response.status_code == 200
        assert response.get_json() == []


def test_get_allaccounts_returns_createdaccounts():
    with app.test_client() as client:
        client.post("/api/accounts", json={"first_name": "Lars", "last_name": "U", "pesel": "11111111111"})
        client.post("/api/accounts", json={"first_name": "K", "last_name": "H", "pesel": "22222222222"})
        response = client.get("/api/accounts")
        data = response.get_json()
        assert len(data) == 2
        assert {a["pesel"] for a in data} == {"11111111111", "22222222222"}


def test_get_account_count():
    with app.test_client() as client:
        assert client.get("/api/accounts/count").get_json()["count"] == 0
        client.post("/api/accounts", json={"first_name": "A", "last_name": "B", "pesel": "33333333333"})
        client.post("/api/accounts", json={"first_name": "C", "last_name": "D", "pesel": "44444444444"})
        assert client.get("/api/accounts/count").get_json()["count"] == 2


def test_get_account_by_pesel_found():
    with app.test_client() as client:
        pesel = "55555555555"
        client.post("/api/accounts", json={"first_name": "Dave", "last_name": "Mustaine", "pesel": pesel})
        response = client.get(f"/api/accounts/{pesel}")
        data = response.get_json()
        assert response.status_code == 200
        assert data["first_name"] == "Dave"
        assert data["pesel"] == pesel


def test_get_account_by_pesel_not_found():
    with app.test_client() as client:
        response = client.get("/api/accounts/99999999999")
        assert response.status_code == 500


def test_update_account_full():
    with app.test_client() as client:
        pesel = "66666666666"
        client.post("/api/accounts", json={"first_name": "Jan", "last_name": "Kowalski", "pesel": pesel})
        client.patch(f"/api/accounts/{pesel}", json={"first_name": "Tomasz", "last_name": "Nowak"})
        updated = registry.search_account_based_on_pesel(pesel)
        assert updated.first_name == "Tomasz"
        assert updated.last_name == "Nowak"


def test_update_account_only_first_name():
    with app.test_client() as client:
        pesel = "77777777777"
        client.post("/api/accounts", json={"first_name": "Adam", "last_name": "Zieliński", "pesel": pesel})
        client.patch(f"/api/accounts/{pesel}", json={"first_name": "Michał"})
        updated = registry.search_account_based_on_pesel(pesel)
        assert updated.first_name == "Michał"
        assert updated.last_name == "Zieliński"


def test_delete_account():
    with app.test_client() as client:
        pesel = "88888888888"
        client.post("/api/accounts", json={"first_name": "X", "last_name": "Y", "pesel": pesel})
        response = client.delete(f"/api/accounts/{pesel}")
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account deleted"