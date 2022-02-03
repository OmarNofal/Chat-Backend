from .dao import dao


class messages_dao(dao):

    def __init__(self, db):
        super().__init__(db, 'messages')
    