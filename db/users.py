from .dao import dao


class users_dao(dao):

    def __init__(self, db):
        super().__init__(db, 'users')

    