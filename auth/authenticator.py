from argparse import ArgumentError
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

        result = self.users.find_one({'phone_number': u.phone_number})
        if result != None:
            raise ArgumentError(argument = None, message='Phone number already registered')
        
        salt = bcrypt.gensalt()
        u.password = bcrypt.hashpw(u.password.encode(), salt).decode()
        
        user_dict = u.as_dict() 
        del user_dict['id']
        result = self.users.insert_one(user_dict)
        if result.acknowledged:
            token = str(uuid.uuid4())
            session = {'user_id': str(result.inserted_id), 'token': token}
            self.sessions.insert_one(session)
            return {'token': token, 'user_id': str(result.inserted_id)}
        else:
            return None
    

    def login(self, credentials: dict):

        phone_number = credentials['phone_number']
        password = credentials['password']

        users = self.users
        result = users.find_one({'phone_number': phone_number})
        if result == None:
            raise ArgumentError(message="Incorrect Phone number")
        print(result)
        if not bcrypt.checkpw(password.encode(), result['password'].encode()):
            raise ArgumentError(message="Incorrect password")
        
        current_session = self.sessions.find_one({'user_id': str(result['_id'])})
        if current_session != None:
            return current_session['token']

        token = str(uuid.uuid4())
        self._insert_session(str(result['_id']), token)
        return token

    def get_user_id(self, token):
        session = self.sessions.find_one({'token': token})
        return session['user_id'] if session != None else None

    def get_token(self, userId):
        session = self.sessions.find_one({'user_id': userId})
        return session['token'] if session != None else None

    def get_instance():
        if authenticator.instance == None:
            database = db.database.app_database.get_instance()
            authenticator.instance = authenticator(database.db)
        return authenticator.instance

    def _insert_session(self, user_id, token):
        return self.sessions.insert_one({'user_id': user_id, 'token': token})


    def _get_session(self, token):
        return self.sessions.find_one({'token': token})
