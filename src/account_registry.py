from src.personal_account import PersonalAccount

class AccountRegistry:
  def __init__(self):
    self.accounts = []

  def add_account(self, account: PersonalAccount):
    self.accounts.append(account)

  def search_account_based_on_pesel(self, pesel):
    for account in self.accounts:
        if account.pesel == pesel:
            return account
    return None

  def get_all_accounts(self):
    return self.accounts
  
  def get_account_count(self):
    return len(self.accounts)

  def remove_account_by_pesel(self, pesel):
    for index, account in enumerate(self.accounts):
        if account.pesel == pesel:
            del self.accounts[index]
            return True
    return False