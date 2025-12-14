import threading

import pytest
import requests
from werkzeug.serving import make_server

from app.api import app, registry


@pytest.fixture(scope="session")
def live_server():
    server = make_server("127.0.0.1", 5005, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:5005"
    server.shutdown()
    thread.join()


@pytest.fixture(autouse=True)
def clean_registry():
    registry.accounts.clear()
    yield


def test_create_account(live_server):
    response = requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "James", "last_name": "Hetfield", "pesel": "89092909825"},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Account created"


def test_get_allaccounts_empty_at_start(live_server):
    response = requests.get(f"{live_server}/api/accounts")
    assert response.status_code == 200
    assert response.json() == []


def test_get_allaccounts_returns_createdaccounts(live_server):
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "Lars", "last_name": "U", "pesel": "11111111111"},
    )
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "K", "last_name": "H", "pesel": "22222222222"},
    )
    response = requests.get(f"{live_server}/api/accounts")
    data = response.json()
    assert len(data) == 2
    assert {a["pesel"] for a in data} == {"11111111111", "22222222222"}


def test_get_account_count(live_server):
    assert requests.get(f"{live_server}/api/accounts/count").json()["count"] == 0
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "A", "last_name": "B", "pesel": "33333333333"},
    )
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "C", "last_name": "D", "pesel": "44444444444"},
    )
    assert requests.get(f"{live_server}/api/accounts/count").json()["count"] == 2


def test_get_account_by_pesel_found(live_server):
    pesel = "55555555555"
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "Dave", "last_name": "Mustaine", "pesel": pesel},
    )
    response = requests.get(f"{live_server}/api/accounts/{pesel}")
    data = response.json()
    assert response.status_code == 200
    assert data["first_name"] == "Dave"
    assert data["pesel"] == pesel


def test_get_account_by_pesel_not_found(live_server):
    response = requests.get(f"{live_server}/api/accounts/99999999999")
    assert response.status_code == 500


def test_update_account_full(live_server):
    pesel = "66666666666"
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "Jan", "last_name": "Kowalski", "pesel": pesel},
    )
    requests.patch(
        f"{live_server}/api/accounts/{pesel}",
        json={"first_name": "Tomasz", "last_name": "Nowak"},
    )
    updated = requests.get(f"{live_server}/api/accounts/{pesel}").json()
    assert updated["first_name"] == "Tomasz"
    assert updated["last_name"] == "Nowak"


def test_update_account_only_first_name(live_server):
    pesel = "77777777777"
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "Adam", "last_name": "Zielinski", "pesel": pesel},
    )
    requests.patch(f"{live_server}/api/accounts/{pesel}", json={"first_name": "Michal"})
    updated = requests.get(f"{live_server}/api/accounts/{pesel}").json()
    assert updated["first_name"] == "Michal"
    assert updated["last_name"] == "Zielinski"


def test_delete_account(live_server):
    pesel = "88888888888"
    requests.post(
        f"{live_server}/api/accounts",
        json={"first_name": "X", "last_name": "Y", "pesel": pesel},
    )
    response = requests.delete(f"{live_server}/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted"