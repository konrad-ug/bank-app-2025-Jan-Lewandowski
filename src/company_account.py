from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Niepoprawny NIP!"
        self.balance = 0.0
        self.oplata_za_express_przelew = 5.0

    def take_loan(self, kwota):
      self.balance = sum(self.historia)
      if (len(self.historia) >= 0 and (-1775 in self.historia) and (self.balance >= 2 * kwota)):
        self.balance += kwota
        return True
      else:
        return False
    
    def is_nip_valid(self, pesel):
        return (len(pesel) == 10 and pesel.isdigit())

