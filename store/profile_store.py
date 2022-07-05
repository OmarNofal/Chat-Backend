from time import sleep
from model.user import user
from db.users import users_dao
from db.database import app_database
from bson import ObjectId
import datetime

class profile_store:
    instance = None
    def __init__(self):
        try:
            db: app_database = app_database.get_instance()
            self.dao = db.get_users_dao()
        except Exception as e:
            print("An error has occured : " + str(e))
    
    def get_user_profile(self, user_id: str) -> user:
        assert(user_id != '')
        try:
            user_profile = self.dao.find_one({'_id': ObjectId(user_id)})
            u = safe_user(user_profile)

            return u
        except Exception as e:
            print(e)
            return None
    
    def search_users(self, query: str):
        result = self.dao.search_users(query= query)
        return list(map(safe_user, result))

    def update_user_profile(self, u: user) -> dict:
        self.dao.update(u)
        return {'result': 'success'}

    def delete_user_profile(self, user_id: str) -> dict:
        self.dao.delete_id(user_id)
        return {'result': 'success'}

    def get_instance():
        if profile_store.instance == None:
            profile_store.instance = profile_store()
        return profile_store.instance

def safe_user(user_profile: dict):
    user_profile['id'] = str(user_profile['_id'])
    del user_profile['_id']

    return user(
        id = user_profile['id'],
        first_name= user_profile['first_name'],
        last_name = user_profile['last_name'],
        birth_date = user_profile['birth_date'],
        phone_number = user_profile['phone_number'],
        password= user_profile['password'],
        country= user_profile['country'],
        status = user_profile['status'],
        pp_id = user_profile['pp_id']
    )