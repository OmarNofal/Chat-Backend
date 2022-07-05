from db.database import app_database
from model.message import message
from db.messages import messages_dao
from bson import ObjectId
from pymongo.results import InsertOneResult

from model.messages_updates import messages_updates

class message_store:
    instance = None
    def __init__(self):
        db = app_database.get_instance()
        self.messages_dao = db.get_messages_dao()
        self.updates_dao = db.get_messages_updates_dao()
    
    def store_message(self, msg: message):
        result: InsertOneResult = self.messages_dao.insert(msg)
        if result.acknowledged:
            return str(result.inserted_id)
        else:
            raise Exception()

    def delete_message(self, msg_id: str):
        return self.messages_dao.delete_one({'_id': ObjectId(msg_id)})

    def get_messages_to(self, user_id: str):
        """
        Returns messages that user_id hasn't seen yet
        """
        return list(self.messages_dao.find({'to_id': user_id}))


    # user_id is the user which is going to receive the update
    def add_received_message(self, user_id: str, message_id: str):
        u_message_status = self._get_message_updates(user_id)
        if (not u_message_status):
            u_message_status = messages_updates(
                id = str(ObjectId()),
                user_id = user_id
            )

        u_message_status.add_received_message(message_id)
        self.updates_dao.update(u_message_status)

    def add_read_message(self, user_id: str, message_id: str):
        u_message_status = self._get_message_updates(user_id)
        if (not u_message_status):
            u_message_status = messages_updates(
                id = str(ObjectId()),
                user_id = user_id
            )
        
        u_message_status.add_read_message(message_id)
        self.updates_dao.update(u_message_status)
        
    def remove_received_messages(self, user_id: str, messages_ids = []):
        u_message_status = self._get_message_updates(user_id)
        if (not u_message_status):
            return

        for id in messages_ids:
            u_message_status.remove_received_message(id)
        self.updates_dao.update(u_message_status)

    def remove_read_messages(self, user_id: str, messages_ids = []):
        
        u_message_status = self._get_message_updates(user_id)
        if (not u_message_status):
            return

        for id in messages_ids:
            u_message_status.remove_read_message(id)
        
        self.updates_dao.update(u_message_status)


    def get_message_updates_to(self, user_id: str) -> messages_updates:
        u_message_updates = self._get_message_updates(user_id)
        return u_message_updates

    def _get_message_updates(self, user_id: str) -> messages_updates:
        u_message_status = self.updates_dao.find_one({'user_id': user_id})
        if (u_message_status == None):
            return None
        else:
            return messages_updates(
                id = str(u_message_status['_id']),
                user_id = user_id,
                received_messages= u_message_status['received_messages'],
                read_messages= u_message_status['read_messages']
            )
        


    def get_instance():
        if message_store.instance == None:
            message_store.instance = message_store()
        return message_store.instance

