import datetime

class user:
    """ represents a user of the application """
    def __init__(self, 
    id: str = None,
    first_name: str = '',
    last_name: str = '',
    birth_date: datetime.date = datetime.date(2001, 7, 23),
    phone_number: str = '+201010000001',
    country: str = 'Egypt',
    status: str = 'Available',
    pp_id: str = None # profile picture id
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.country = country
        self.status = status
        self.pp_id = pp_id
    
    def as_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'phone_number': self.phone_number,
            'country': self.country,
            'status': self.status,
            'pp_id': self.pp_id
        }
