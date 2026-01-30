from src.account import Account
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
import pytest

class TestRegistry:
  @pytest.fixture
  def personal_account1(self):
    personal_account = PersonalAccount("John", "Doe", "12312312312")
    return personal_account
  @pytest.fixture
  def personal_account2(self):
    personal_account = PersonalAccount("David", "Clinton", "78978978978")
    return personal_account
  @pytest.fixture
  def account_registry(self):
    account_registry = AccountRegistry()
    return account_registry

  def test_add_account(self, account_registry: AccountRegistry, personal_account1: PersonalAccount, personal_account2: PersonalAccount):
    account_registry.add_account(personal_account1)
    account_registry.add_account(personal_account2)
    assert account_registry.accounts == [personal_account1, personal_account2]

  def test_search_account_based_on_valid_pesel(self, account_registry: AccountRegistry, personal_account1: PersonalAccount, personal_account2: PersonalAccount):
    account_registry.add_account(personal_account1)
    account_registry.add_account(personal_account2)
    assert account_registry.search_account_based_on_pesel("12312312312") == personal_account1
    assert account_registry.search_account_based_on_pesel("78978978978") == personal_account2

  def test_search_account_based_on_invalid_pesel(self, account_registry: AccountRegistry):
    invalid_personal_account = PersonalAccount("name", "lastname", "123")
    assert account_registry.search_account_based_on_pesel("123") == None

  def test_get_all_accounts(self, account_registry: AccountRegistry, personal_account1: PersonalAccount, personal_account2: PersonalAccount):
    account_registry.add_account(personal_account1)
    account_registry.add_account(personal_account2)
    assert account_registry.get_all_accounts() == [personal_account1,personal_account2]
  
  def test_get_all_accounts_empty(self, account_registry: AccountRegistry):
    assert account_registry.get_all_accounts() == []
  
  def test_get_account_count(self, account_registry: AccountRegistry, personal_account1: PersonalAccount, personal_account2: PersonalAccount):
    account_registry.add_account(personal_account1)
    account_registry.add_account(personal_account2)
    assert account_registry.get_account_count() == 2

  def test_get_account_count_empty(self, account_registry: AccountRegistry):
    assert account_registry.get_account_count() == 0

  def test_remove_account_by_valid_pesel(self, account_registry: AccountRegistry, personal_account1: PersonalAccount, personal_account2: PersonalAccount):
    account_registry.add_account(personal_account1)
    account_registry.add_account(personal_account2)
    assert account_registry.remove_account_by_pesel("12312312312") is True
    assert account_registry.get_account_count() == 1
    assert account_registry.search_account_based_on_pesel("12312312312") is None
    assert account_registry.accounts == [personal_account2]

  def test_remove_account_by_invalid_pesel(self, account_registry: AccountRegistry, personal_account1: PersonalAccount, personal_account2: PersonalAccount):
    account_registry.add_account(personal_account1)
    account_registry.add_account(personal_account2)
    assert account_registry.remove_account_by_pesel("00000000000") is False
    assert account_registry.get_account_count() == 2
    assert account_registry.accounts == [personal_account1, personal_account2]