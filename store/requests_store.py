from model.user import user
from model.request import request
from model.friends import friends
from db.users import users_dao
from db.requests import requests_dao
from db.database import app_database
from db.friends import friends_dao
from bson import ObjectId
import datetime
import pymongo

class requests_store:

    instance = None
    def __init__(self):
        db = app_database.get_instance()
        self.requests_dao: requests_dao = db.get_requests_dao()
        self.friends_dao: friends_dao = db.get_friends_dao()
    
    def send_request(self, from_id: str, to_id: str, time = datetime.datetime.now()) -> dict:
        req = request(sender_id= from_id, receiver_id= to_id, time= time)

        try:
            result = self.requests_dao.insert(req)
            if result.acknowledged:
                return {'result': 'success', 'friend_request_id': str(result.inserted_id)}
            else:
                return {'result': 'error', 'message': 'error occurred submitting friend request'}
        except Exception as e:
            return {'result': 'error', 'message': 'error occurred: ' + str(e)}
    
    def accept_request(self, friend_request_id: str) -> dict:
        friend_request = self.requests_dao.find_one({'_id': ObjectId(friend_request_id)})
        if not friend_request:
            return {'result': 'error', 'message': 'this friend request does not exist'}
        
        sender_id = friend_request['sender_id']
        receiver_id = friend_request['receiver_id']


        result = self._add_friends(sender_id, receiver_id)
        if result.acknowledged:
            self.requests_dao.delete_id(friend_request_id)
            return {'result': 'success'}
        else:
            return {'result': 'error', 'message': 'error occurred while accepting request #'+ friend_request_id}
        
    def _add_friends(self, u1_id: str, u2_id: str):
        
        if u2_id < u1_id:
            u1_id, u2_id = u2_id, u1_id
        
        friend_relation = friends(u1_id= u1_id, u2_id= u2_id)
        
        return self.friends_dao.insert(friend_relation)
        
    def get_requests_from(self, user_id: str):
        return list(self.requests_dao.find({'sender_id': user_id}))

    def get_requests_to(self, user_id: str):
        return list(self.requests_dao.find({'receiver_id': user_id}))

    def get_user_requests(self, user_id: str):
        return self.get_requests_from(user_id) + self.get_requests_to(user_id)

    def cancel_request(self, friend_request_id: str):
        try:
            result: pymongo.results.DeleteResult = self.requests_dao.delete_id(friend_request_id)
            if result.deleted_count >= 1:
                return {'result': 'success'}
            else:
                return {'result': 'error', 'message':'couldn\'t delete friend request'}
        except Exception as e:
            return {'result': 'error', 'message':'couldn\'t delete friend request'}
    
    def get_instance():
        if requests_store.instance == None:
            requests_store.instance = requests_store()
        return requests_store.instance