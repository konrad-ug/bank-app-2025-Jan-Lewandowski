from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = PersonalAccount(data["first_name"], data["last_name"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [{"first_name": acc.first_name, "last_name": acc.last_name, "pesel":acc.pesel, "balance": acc.balance} for acc in accounts]
    
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.get_account_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    found_person = registry.search_account_based_on_pesel(pesel)
    return (
        jsonify(
            {
                "first_name": found_person.first_name,
                "last_name": found_person.last_name,
                "pesel": found_person.pesel,
                "balance": found_person.balance,
            }
        ),
        200,
)

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    found_person = registry.search_account_based_on_pesel(pesel)

    if "first_name" in data:
        found_person.first_name = data["first_name"]
    if "last_name" in data:
        found_person.last_name = data["last_name"]
    return (
        jsonify(
            {
                "message": "Account updated",
                "account": {
                    "pesel": found_person.pesel,
                    "first_name": found_person.first_name,
                    "last_name": found_person.last_name,
                },
            }
        ),
        200,
    )

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    found_person = registry.search_account_based_on_pesel(pesel)
    found_person = None
    return jsonify({"message": "Account deleted"}), 200