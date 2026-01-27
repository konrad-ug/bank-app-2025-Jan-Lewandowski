from behave import *

import requests


URL = "http://127.0.0.1:5005"
@step('I create an account using name: "{name}", last name: "{last_name}", pesel:"{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = { "first_name": f"{name}",
    "last_name": f"{last_name}",
    "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json = json_body)
    assert create_resp.status_code == 201
@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()

    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")
@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    create_resp = requests.get(URL + "/api/accounts/count")
    assert create_resp.status_code == 200
    assert create_resp.json()["count"] == int(count)
@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404
@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")

    field_mapping = {
        "name": "first_name",
        "surname": "last_name"
    }

    json_body = { field_mapping[field]: value }
    response = requests.patch(URL + f"/api/accounts/{pesel}", json = json_body)
    assert response.status_code == 200
@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account_data = response.json()
    if field == "name":
        assert account_data["first_name"] == value
    elif field == "surname":
        assert account_data["last_name"] == value
    else:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")