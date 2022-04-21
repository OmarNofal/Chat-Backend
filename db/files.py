from .dao import dao


class files_dao(dao):

    def __init__(self, db):
        super().__init__(db, 'files')
        