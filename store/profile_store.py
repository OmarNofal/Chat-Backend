from model.user import user
from db.users import users_dao
from db.database import app_database
from bson import ObjectId

class profile_store:
    instance = None
    def __init__(self):
        try:
            db: app_database = app_database.get_instance()
            self.dao = db.get_users_dao()
        except Exception as e:
            print("An error has occured : " + str(e))
    
    def get_user_profile(self, user_id: str) -> dict:
        assert(user_id != '')
        try:
            user_profile = self.dao.find_one({'_id': ObjectId(user_id)})
            del user_profile['password']

            user_profile['id'] = str(user_profile['_id'])
            del user_profile['_id']

            return user_profile
        except Exception as e:
            return {'result': 'error', 'message': 'An error has occurred ' + str(e)}
    
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