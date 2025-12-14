import os
from datetime import date

import requests

from src.account import Account


class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.balance = 0.0
        self.oplata_za_express_przelew = 5.0

        if not self.is_nip_valid(nip):
            self.nip = "Niepoprawny NIP!"
            self.is_vat_active = None
            return

        self.nip = nip
        self.is_vat_active = self.check_vat_status(nip)

    def take_loan(self, kwota):
        self.balance = sum(self.historia)
        if (len(self.historia) >= 0 and (-1775 in self.historia) and (self.balance >= 2 * kwota)):
            self.balance += kwota
            return True
        return False

    def is_nip_valid(self, nip):
        return len(nip) == 10 and nip.isdigit()

    def check_vat_status(self, nip):
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl").rstrip("/")
        today = date.today().strftime("%Y-%m-%d")
        url = f"{base_url}/api/search/nip/{nip}?date={today}"

        response = requests.get(url, timeout=10)
        print(f"MF response for {nip}: {response.text}")

        if response.status_code == 404:
            raise ValueError("Company not registered!!")

        response.raise_for_status()
        data = response.json()
        subject = data.get("result", {}).get("subject")
        if not subject:
            raise ValueError("Company not registered!!")

        return subject.get("statusVat") == "Czynny"

