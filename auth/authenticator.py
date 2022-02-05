import bcrypt
import db.database
import pymongo
import uuid
from model.user import user

class authenticator:
    instance = None
    def __init__(self, db):
        self.users = db['users']
        self.sessions = db['sessions']
 
    def register(self, u: user):

        try:
            result = self.users.find_one({'phone_number': u.phone_number})
            if result != None:
                return {'result': 'error', 'message': 'Phone number already registered'}
            
            salt = bcrypt.gensalt()
            u.password = bcrypt.hashpw(u.password.encode(), salt).decode()
            
            user_dict = u.as_dict() 
            del user_dict['id']
            result = self.users.insert_one(user_dict)
            if result.acknowledged:
                token = str(uuid.uuid4())
                session = {'user_id': str(result.inserted_id), 'token': token}
                self.sessions.insert_one(session)
                return {'result': 'success', 'token': token, 'user_id': str(result.inserted_id)}
            else:
                return {'result': 'error', 'message': 'Some error has occured'}
        except Exception as e:
            return {'result': 'error', 'message': 'An error occured: ' + str(e)}

    def login(self, credentials: dict):
        try:
            phone_number = credentials['phone_number']
            password = credentials['password']

            users = self.users
            result = users.find_one({'phone_number': phone_number})
            if result == None:
                return {'result': 'error', 'message': 'Phone number doesn\'t exist'}
            print(result)
            if not bcrypt.checkpw(password.encode(), result['password'].encode()):
                return {'result': 'error', 'message': 'Invalid password'}
            
            current_session = self.sessions.find_one({'user_id': str(result['_id'])})
            if current_session != None:
                return {'result': 'success', 'token': current_session['token']}

            token = str(uuid.uuid4())
            self._insert_session(str(result['_id']), token)
            return {'result': 'success', 'token': token}
        except Exception as e:
            
            return {'result': 'error', 'message': 'An error occured: ' + str(e)}

    def get_user_id(self, token):
        session = self.sessions.find_one({'token': token})
        return session['user_id'] if session != None else None

    def get_instance():
        if authenticator.instance == None:
            database = db.database.app_database.get_instance()
            authenticator.instance = authenticator(database)
        return authenticator.instance

    def _insert_session(self, user_id, token):
        return self.sessions.insert_one({'user_id': user_id, 'token': token})


    def _get_session(self, token):
        return self.sessions.find_one({'token': token})
