class Account:
    def __init__(self):
        self.historia = []
    
    def get(self, kwota):
        self.balance += kwota if kwota >= 0 else self.balance
        self.historia.append(kwota)
        return self.balance

    def send(self, kwota):
        if kwota > 0:
            self.balance -= kwota if self.balance >= kwota else self.balance
        self.historia.append(-kwota)    
        return self.balance

    def show_transfers_history(self):
        return self.historia

    def is_express_send_correct(self, kwota):
        return self.balance >= kwota and kwota > 0
