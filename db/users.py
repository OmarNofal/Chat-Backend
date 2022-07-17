from .dao import dao


class users_dao(dao):

    def __init__(self, db):
        super().__init__(db, 'users')

    def search_users(self, query: str):
        return self.collection.find ( {'$text': {'$search': query}} )

    