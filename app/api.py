from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    if registry.search_account_based_on_pesel(data["pesel"]):
        return jsonify({"message": "Account with this PESEL already exists"}), 409
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
    removed = registry.remove_account_by_pesel(pesel)
    if not removed:
        return jsonify({"message": "Account not found"}), 404
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer_funds(pesel):
    data = request.get_json()

    if registry.search_account_based_on_pesel(pesel) is None:
        return jsonify({"message": "Account not found"}), 404
    
    found_person = registry.search_account_based_on_pesel(pesel)

    amount = data["amount"]

    if data["type"] == "incoming":
        found_person.balance += amount
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    elif data["type"] == "outgoing":
        found_person.balance -= amount
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    elif data["type"] == "express":
        found_person.balance -= (amount + found_person.oplata_za_express_przelew)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    else:
        return jsonify({"message": "Nieznany typ przelewu"}), 400