from .dao import dao

class messages_updates_dao(dao):

    def __init__(self, db):
        super().__init__(db, 'messages_updates')
    