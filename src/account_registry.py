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

  def return_all_accounts(self):
    return self.accounts
  
  def return_amount_of_accounts(self):
    return len(self.accounts)