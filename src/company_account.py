from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Niepoprawny NIP!"
        self.balance = 0.0
        self.oplata_za_express_przelew = 5.0
    
    def express_send(self, kwota):
        if self.is_express_send_correct(kwota):
            self.balance -= (kwota + 5)
            return self.balance
        else:
            return "Not enough money"

    def is_nip_valid(self, pesel):
        return (len(pesel) == 10 and pesel.isdigit())