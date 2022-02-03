from .dao import dao


class media_dao(dao):
    def __init__(self, db):
        super().__init__(self, db, 'media')