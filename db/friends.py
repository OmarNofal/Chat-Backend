from .dao import dao


class friends_dao(dao):

    def __init__(self, db):
        super().__init__(db, 'friends')
        