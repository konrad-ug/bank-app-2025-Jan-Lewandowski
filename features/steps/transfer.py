from behave import *
import requests

URL = "http://127.0.0.1:5005"

@step('I send a transfer request to pesel "{pesel_to}" with amount "{amount}" type "{transfer}"')
def send_transfer_request(context, pesel_to, amount, transfer):
    json_body = {
        "amount": float(amount),
        "type": transfer
        }
    response = requests.post(f"{URL}/api/accounts/{pesel_to}/transfer", json=json_body)
    assert response.status_code == 200

@when('I send a transfer request to pesel "{pesel_to}" with amount:"{amount}" type:"{transfer}"')
def send_transfer_request_colon(context, pesel_to, amount, transfer):
    json_body = {
        "amount": float(amount),
        "type": transfer
        }
    response = requests.post(f"{URL}/api/accounts/{pesel_to}/transfer", json=json_body)
    assert response.status_code == 200

@then('Account with pesel "{pesel}" has {expected_balance} cash')
def check_account_cash(context, pesel, expected_balance):
    response = requests.get(f"{URL}/api/accounts/{pesel}")
    assert response.status_code == 200
    account_data = response.json()
    actual_balance = account_data["balance"]
    assert actual_balance == float(expected_balance)