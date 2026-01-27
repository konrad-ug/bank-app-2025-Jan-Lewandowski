import time

import pytest

from app.api import app, registry


@pytest.fixture()
def client():
    registry.accounts = []
    with app.test_client() as client:
        yield client


def test_create_and_delete_accounts_perf(client):
    for i in range(100):
        pesel = f"8000000{i:05d}"

        start = time.perf_counter()
        create_resp = client.post(
            "/api/accounts",
            json={"first_name": "Perf", "last_name": "User", "pesel": pesel},
        )
        duration = time.perf_counter() - start
        assert create_resp.status_code == 201
        assert duration < 0.5

        start = time.perf_counter()
        delete_resp = client.delete(f"/api/accounts/{pesel}")
        duration = time.perf_counter() - start
        assert delete_resp.status_code == 200
        assert duration < 0.5


def test_incoming_transfers_perf(client):
    pesel = "12345678901"

    start = time.perf_counter()
    create_resp = client.post(
        "/api/accounts",
        json={"first_name": "Perf", "last_name": "Depositor", "pesel": pesel},
    )
    duration = time.perf_counter() - start
    assert create_resp.status_code == 201
    assert duration < 0.5

    for _ in range(100):
        start = time.perf_counter()
        transfer_resp = client.post(
            f"/api/accounts/{pesel}/transfer",
            json={"type": "incoming", "amount": 10.0},
        )
        duration = time.perf_counter() - start
        assert transfer_resp.status_code == 200
        assert duration < 0.5

    balance_resp = client.get(f"/api/accounts/{pesel}")
    assert balance_resp.status_code == 200
    assert balance_resp.get_json().get("balance") == 1000.0
