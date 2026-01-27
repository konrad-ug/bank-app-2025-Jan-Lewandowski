from datetime import date
from smtp.smtp import SMTPClient

class Account:
    def __init__(self):
        self.historia = []

    def get(self, kwota):
        if kwota > 0:
            self.balance += kwota
            self.historia.append(kwota)
        return self.balance

    def send(self, kwota):
        if kwota > 0 and self.balance >= kwota:
            self.balance -= kwota
            self.historia.append(-kwota)
        return self.balance

    def express_send(self, kwota):
        if kwota <= 0:
            return "Not enough money"

        total = kwota + self.oplata_za_express_przelew

        if self.balance - total >= -self.oplata_za_express_przelew:
            self.balance -= total
            self.historia.append(-total)
            return self.balance

        return "Not enough money"

    def is_express_send_correct(self, kwota):
        return self.balance >= kwota and kwota > 0

    def send_history_via_email(self, email_address):
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"

        if hasattr(self, "company_name"):
            prefix = "Company account history"
        else:
            prefix = "Personal account history"
        text = f"{prefix}: {self.historia}"

        return SMTPClient.send(subject, text, email_address)