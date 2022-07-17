import threading
from socket_server.connection import connection
from socket_server.messages.socket_message import json_message
from . import initializer
import firebase_admin.messaging as messaging
from utils.constants import *
from socket_server.connection_pool import connection_pool
from auth.authenticator import authenticator

class Notifier:
    """
    This class is responsible for notifying users of new messages through firebase
    """

    def __init__(self) -> None:
        return

    
    def notify_new_friend_request(self, destination_user_id: str, sending_user_name: str):
        threading.Thread(target = self._notify_new_friend_request, args=[destination_user_id, sending_user_name]).start()

    def _notify_new_friend_request(self, destination_user_id: str, sending_user_name: str):
        token = self._get_user_topic_name(destination_user_id)
        message = messaging.Message(
            data = {
                FB_MESSAGE_TYPE: FB_TYPE_NEW_FRIEND_REQUEST,
                FB_USER_NAME: sending_user_name
            },
            topic = token
        )
        messaging.send(message)
        
    def notify_accepted_friend_request(self, destination_user_id: str, accepting_user_name: str):
        threading.Thread(target = self._notify_accepted_friend_request, args=[destination_user_id, accepting_user_name]).start()

    def _notify_accepted_friend_request(self, destination_user_id: str, accepting_user_name: str):
        token = self._get_user_topic_name(destination_user_id)
        message = messaging.Message(
            data = {
                FB_MESSAGE_TYPE: FB_TYPE_ACCEPTED_FRIEND_REQUEST,
                FB_USER_NAME: accepting_user_name
            },
            topic = token
        )

        messaging.send(message)


    def notify_new_messages(self, user_id: str):
        threading.Thread(target = self._notify_new_messages, args=[user_id]).start()
        

    def _notify_new_messages(self, user_id:str):


        # if user is connected, send using sockets
        user_connection: connection = connection_pool.get_instance().get_connection(user_id) 
        if user_connection is not None:
            message = json_message(REQUEST_PENDING_MESSAGES, content = {}, header = {})
            user_connection.send_message(message)
            return

        token = self._get_user_topic_name(user_id)
        # user is not connected. send using firebase
        print("Sending firebase message")
        message = messaging.Message(
            data = {
                FB_MESSAGE_TYPE: FB_TYPE_NEW_MESSAGES
            },
            topic = token,
            android= messaging.AndroidConfig(priority="high")
        )

        messaging.send(message)

    
    # the topic which the client subscribes to to recieve his messages
    # for now this is the user token
    def _get_user_topic_name(self, userId: str) -> str:
        token = authenticator.get_instance().get_token(userId)
        if not token:
            return 'null'
        return token