class Account:
    def get(self, kwota):
        self.balance += kwota if kwota >= 0 else self.balance
        return self.balance

    def send(self, kwota):
        if kwota > 0:
            self.balance -= kwota if self.balance >= kwota else self.balance
        return self.balance

    def is_express_send_correct(self, kwota):
        return self.balance >= kwota and kwota > 0
