from src.account import Account



class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        account.balance = 100.0
        assert account.balance == 100.0
        account.balance += 100.0
        assert account.balance == 200.0
        assert account.pesel == "Invalid"

    def test_account_pesel_too_short(self):
        account = Account("John", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_account_pesel_too_short(self):
        account = Account("John", "Doe", "123123123123123213")
        assert account.pesel == "Invalid"

    def test_account_pesel_good(self):
        account = Account("John", "Doe", "12312312312")
        assert account.pesel == "12312312312"

    def test_account_pesel_non_numeric(self):
        account = Account("John", "Doe", "123123abcd")
        assert account.pesel == "Invalid"

    def test_account_promo_valid(self):
        account = Account("John", "Doe", "12312312312", "PROM_abc")
        assert account.balance == 50.0

    def test_account_promo_wrong_prefix(self):
        account = Account("John", "Doe", "12312312312","PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long(self):
        account = Account("John", "Doe", "12312312312", "PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_wrong_format(self):
        account = Account("John", "Doe", "12312312312", "INVALID_FORMAT")
        assert account.balance == 0.0 

    def test_account_promo_suffix_too_short(self):
        account = Account("John", "Doe", "12312312312", "PROM_a")
        assert account.balance == 0.0
        
    def test_account_promo_valid_young(self):
        account = Account("John", "Doe", "65123456789", "PROM_abc")
        assert account.balance == 50.0
        
    def test_account_promo_valid_young_21st_century(self):
        account = Account("John", "Doe", "23345678901", "PROM_abc")
        assert account.balance == 50.0

    def test_account_promo_wrong_prefix_young(self):
        account = Account("John", "Doe", "PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long_young(self):
        account = Account("John", "Doe", "65123456789","PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_wrong_format_young(self):
        account = Account("John", "Doe", "65123456789","INVALID_FORMAT")
        assert account.balance == 0.0 

    def test_account_promo_suffix_too_short_young(self):
        account = Account("John", "Doe", "65123456789","PROM_a")
        assert account.balance == 0.0
        
    def test_account_promo_valid_old(self):
        account = Account("John", "Doe", "55103456789", "PROM_abc")
        assert account.balance == 0.0

    def test_account_promo_wrong_prefix_old(self):
        account = Account("John", "Doe", "55123456789", "PRO_abc")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long_old(self):
        account = Account("John", "Doe", "55123456789","PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_wrong_format_old(self):
        account = Account("John", "Doe", "55123456789","INVALID_FORMAT")
        assert account.balance == 0.0 

    def test_account_promo_suffix_too_short_old(self):
        account = Account("John", "Doe", "55123456789","PROM_a")
        assert account.balance == 0.0

    def test_account_get_positive_amount(self):
        account = Account("John", "Doe", "55123456789","PROM_a")
        assert account.get(50.0) == 50.0
        assert account.balance == 50.0

    def test_account_get_negative_amount(self):
        account = Account("John", "Doe", "55123456789","PROM_a")
        assert account.get(-50.0) == 0.0
        assert account.balance == 0.0   

    def test_account_send_enough_money(self):
        account = Account("John", "Doe", "55123456789","PROM_a")
        account.balance = 50.0
        account.send(30.0)
        assert account.balance == 20.0
    
    def test_account_send_not_enough_money(self):
        account = Account("John", "Doe", "55123456789","PROM_a")
        account.balance = 0.0

        assert account.send(30.0) == 0.0

    def test_account_send_negative_amount(self):
        account = Account("John", "Doe", "55123456789","PROM_a")
        account.balance = 30.0
        account.send(-20.0)
        assert account.balance == 30.0


class TestCompany:
    def test_company_account_valid_pesel(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.nip == "1231231231"
    
    def test_company_account_wrong_pesel(self):
        company_account = CompanyAccount("firma", "1231213213231231abc")
        assert company_account.nip == "Niepoprawny NIP!"

    
    def test_account_get_positive_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.get(50.0) == 50.0
        assert company_account.balance == 50.0

    def test_account_get_negative_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.get(-50.0) == 0.0
        assert company_account.balance == 0.0   

    def test_account_send_enough_money(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.send(30.0)
        assert company_account.balance == 20.0
    
    def test_account_send_not_enough_money(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 0.0

        assert company_account.send(30.0) == 0.0

    def test_account_send_negative_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 30.0
        company_account.send(-20.0)
        assert company_account.balance == 30.0