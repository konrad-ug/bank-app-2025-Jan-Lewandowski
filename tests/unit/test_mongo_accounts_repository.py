from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount


def test_save_all_clears_and_upserts(mocker):
    mock_collection = mocker.Mock()
    repo = MongoAccountsRepository(collection=mock_collection)

    account1 = PersonalAccount("A", "B", "11111111111")
    account2 = PersonalAccount("C", "D", "22222222222")

    repo.save_all([account1, account2])

    mock_collection.delete_many.assert_called_once_with({})
    assert mock_collection.update_one.call_count == 2


def test_load_all_builds_accounts(mocker):
    mock_collection = mocker.Mock()
    account1 = PersonalAccount("A", "B", "11111111111")
    account2 = PersonalAccount("C", "D", "22222222222")
    mock_collection.find.return_value = [account1.to_dict(), account2.to_dict()]

    repo = MongoAccountsRepository(collection=mock_collection)
    loaded = repo.load_all()

    assert len(loaded) == 2
    assert loaded[0].pesel == "11111111111"
    assert loaded[1].pesel == "22222222222"
