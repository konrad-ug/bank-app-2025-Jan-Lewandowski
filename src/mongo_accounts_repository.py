import os
from pymongo import MongoClient
from src.personal_account import PersonalAccount


class MongoAccountsRepository():
    def __init__(self, mongo_url=None, db_name="app_db", collection_name=None, collection=None):
        if collection is not None:
            self.collection = collection
            return
        mongo_url = mongo_url or os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        db_name = db_name or os.getenv("MONGO_DB_NAME", "app_db")
        collection_name = collection_name or os.getenv("MONGO_COLLECTION_NAME", "accounts")
        client = MongoClient(mongo_url)
        db = client[db_name]
        self.collection = db[collection_name]

    def save_all(self, accounts):
        self.collection.delete_many({})
        for account in accounts:
            self.collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.__dict__},
                upsert=True
            )

    def load_all(self):
        accounts = []
        for doc in self.collection.find():
            accounts.append(PersonalAccount.from_dict(doc))
        return accounts