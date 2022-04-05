class BaseAccountClass():
    def __init__(self, **kwargs):
        self.organization = kwargs.get('Organization')
        self.id = kwargs.get('Id')
        self.first_name = kwargs.get('FirstName')
        self.last_name = kwargs.get('LastName')
        self.email = kwargs.get('Email')
        self.country = kwargs.get('Country')
        self.number = kwargs.get('PhoneNumber')
        self.validate()

    def check(self):
        if (self.organization and
                self.id and
                self.first_name and
                self.email and
                self.country) and \
                self.country.lower() in self.organization.lower():
            return True
        return False

    def account_dict(self):
        return {
            'Organization': self.organization,
            'Id': self.id,
            'FirstName': self.first_name,
            'LastName': self.last_name,
            'Email': self.email,
            'Country': self.country,
            'PhoneNumber': self.number,
            'AccountType': self.account_type
        }
    
    def validate(self):
        l_country = self.country.split(' ')
        if len(l_country) > 0:
            for idx, word in enumerate(l_country):
                if word.lower() in ['of', 'the', 'former', 'part']:
                    l_country[idx] = word.lower()
                else:
                    l_country[idx] = word.capitalize()
                f_county = ' '.join(l_country)
            self.country = f_county


class Athlete(BaseAccountClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_type = 'Athlete'


class Orchestrator(BaseAccountClass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_type = 'Orchestrator'


class Tester(BaseAccountClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_type = 'Tester'
        
class Admin(BaseAccountClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.organization = 'WADA'
        self.country = 'WADA'
        self.account_type = 'Admin'
