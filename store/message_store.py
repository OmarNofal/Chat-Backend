from db.database import app_database
from model.message import message
from db.messages import messages_dao
from bson import ObjectId

class message_store:
    instance = None
    def __init__(self):
        db = app_database.get_instance()
        self.dao = db.get_messages_dao()
    
    def store_message(self, msg: message):
        result = self.dao.insert(msg)
        if result.acknowledged:
            return {'result': 'success', 'message_id': result.insertedId}
        return {'result': 'error', 'message': 'Error occured while sending message'}

    def delete_message(self, msg_id: str):
        return self.dao.delete_one({'_id': ObjecetId(msg_id)})

    def get_messages_to(self, user_id: str):
        """
        Returns messages that user_id hasn't seen yet
        """
        return list(self.dao.find({'to_id': user_id}))

    def get_instance():
        if message_store.instance == None:
            message_store.instance = message_store()
        return message_store.instance

