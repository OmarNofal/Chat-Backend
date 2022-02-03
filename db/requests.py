from .dao import dao


class requests_dao(dao):

    def __init__(self, db):
        super().__init__(self, db, 'requests')
        