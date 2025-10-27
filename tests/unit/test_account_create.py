from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestPersonalAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        account.balance = 100.0
        assert account.balance == 100.0
        account.balance += 100.0
        assert account.balance == 200.0
        assert account.pesel == "Invalid"

    def test_account_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "123")
        assert account.pesel == "Invalid"

    def test_account_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "123123123123123213")
        assert account.pesel == "Invalid"

    def test_account_pesel_good(self):
        account = PersonalAccount("John", "Doe", "12312312312")
        assert account.pesel == "12312312312"

    def test_account_pesel_non_numeric(self):
        account = PersonalAccount("John", "Doe", "123123abcd")
        assert account.pesel == "Invalid"

    def test_account_promo_valid(self):
        account = PersonalAccount("John", "Doe", "12312312312", "PROM_abc")
        assert account.balance == 50.0

    def test_account_promo_wrong_prefix(self):
        account = PersonalAccount("John", "Doe", "12312312312","PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long(self):
        account = PersonalAccount("John", "Doe", "12312312312", "PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_wrong_format(self):
        account = PersonalAccount("John", "Doe", "12312312312", "INVALID_FORMAT")
        assert account.balance == 0.0 

    def test_account_promo_suffix_too_short(self):
        account = PersonalAccount("John", "Doe", "12312312312", "PROM_a")
        assert account.balance == 0.0
        
    def test_account_promo_valid_young(self):
        account = PersonalAccount("John", "Doe", "65123456789", "PROM_abc")
        assert account.balance == 50.0
        
    def test_account_promo_valid_young_21st_century(self):
        account = PersonalAccount("John", "Doe", "23345678901", "PROM_abc")
        assert account.balance == 50.0

    def test_account_promo_wrong_prefix_young(self):
        account = PersonalAccount("John", "Doe", "PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long_young(self):
        account = PersonalAccount("John", "Doe", "65123456789","PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_wrong_format_young(self):
        account = PersonalAccount("John", "Doe", "65123456789","INVALID_FORMAT")
        assert account.balance == 0.0 

    def test_account_promo_suffix_too_short_young(self):
        account = PersonalAccount("John", "Doe", "65123456789","PROM_a")
        assert account.balance == 0.0
        
    def test_account_promo_valid_old(self):
        account = PersonalAccount("John", "Doe", "55103456789", "PROM_abc")
        assert account.balance == 0.0

    def test_account_promo_wrong_prefix_old(self):
        account = PersonalAccount("John", "Doe", "55123456789", "PRO_abc")
        assert account.balance == 0.0

    def test_account_promo_suffix_too_long_old(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_abcdef")
        assert account.balance == 0.0

    def test_account_promo_wrong_format_old(self):
        account = PersonalAccount("John", "Doe", "55123456789","INVALID_FORMAT")
        assert account.balance == 0.0 

    def test_account_promo_suffix_too_short_old(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        assert account.balance == 0.0

    def test_account_get_positive_amount(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        assert account.get(50.0) == 50.0
        assert account.balance == 50.0

    def test_account_get_negative_amount(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        assert account.get(-50.0) == 0.0
        assert account.balance == 0.0   

    def test_account_send_enough_money(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        account.balance = 50.0
        account.send(30.0)
        assert account.balance == 20.0
    
    def test_account_send_not_enough_money(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        account.balance = 0.0

        assert account.send(30.0) == 0.0

    def test_account_send_negative_amount(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        account.balance = 30.0
        account.send(-20.0)
        assert account.balance == 30.0

    def test_account_express_send_enough_money(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        account.balance = 50.0
        account.express_send(30.0)
        assert account.balance == 19.0
    
    def test_account_express_send_not_enough_money(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        account.balance = 0.0
        assert account.express_send(30.0) == "Not enough money"

    def test_account_express_send_negative_amount(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        account.balance = 30.0
        account.express_send(-20.0)
        assert account.balance == 30.0

    def test_account_express_send_negative_balance(self):
        account = PersonalAccount("John", "Doe", "55123456789","PROM_a")
        account.balance = 5.0
        account.express_send(5.0)
        assert account.balance == -1.0



class TestCompany:
    def test_company_account_valid_pesel(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.nip == "1231231231"
    
    def test_company_account_wrong_pesel(self):
        company_account = CompanyAccount("firma", "1231213213231231abc")
        assert company_account.nip == "Niepoprawny NIP!"

    
    def test_company_account_get_positive_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.get(50.0) == 50.0
        assert company_account.balance == 50.0

    def test_company_account_get_negative_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        assert company_account.get(-50.0) == 0.0
        assert company_account.balance == 0.0   

    def test_company_account_send_enough_money(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.send(30.0)
        assert company_account.balance == 20.0
    
    def test_company_account_send_not_enough_money(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 0.0

        assert company_account.send(30.0) == 0.0

    def test_company_account_send_negative_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 30.0
        company_account.send(-20.0)
        assert company_account.balance == 30.0

    def test_company_account_express_send_enough_money(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 50.0
        company_account.express_send(30.0)
        assert company_account.balance == 15.0
    
    def test_company_account_express_send_not_enough_money(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 0.0
        assert company_account.express_send(30.0) == "Not enough money"

    def test_company_account_express_send_negative_amount(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 30.0
        company_account.express_send(-20.0)
        assert company_account.balance == 30.0

    def test_account_express_send_negative_balance(self):
        company_account = CompanyAccount("firma", "1231231231")
        company_account.balance = 5.0
        company_account.express_send(6.0)
        assert company_account.balance == 5.0