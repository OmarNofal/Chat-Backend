from pymongo import MongoClient

from db.files import files_dao
from .users import users_dao
from .messages import messages_dao
from .media import media_dao
from .requests import requests_dao
from .friends import friends_dao

class app_database:
    instance = None
    def __init__(self, host = 'localhost', port = 27017, db_name = 'chat'):
        self.client = MongoClient(host = host, port = port)
        self.db = self.client[db_name]
        
        
    def get_users_dao(self) -> users_dao:
        return users_dao(self.db)

    def get_media_dao(self) -> media_dao:
        return media_dao(self.db)

    def get_messages_dao(self) -> messages_dao:
        return messages_dao(self.db)

    def get_requests_dao(self) -> requests_dao:
        return requests_dao(self.db)
    
    def get_friends_dao(self) -> friends_dao:
        return friends_dao(self.db)

    def get_files_dao(self) -> files_dao:
        return files_dao(self.db)

    def get_instance(host = 'localhost', port = 27017, db_name = 'chat'):
        if app_database.instance == None:
            app_database.instance = app_database(host, port, db_name)
        return app_database.instance