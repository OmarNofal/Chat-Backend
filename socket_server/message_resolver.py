

import base64
from datetime import datetime
from queue import Queue
from socket import socket
import json
from this import s


from socket_server.connection import connection
from utils.constants import *
from auth.authenticator import authenticator
from files_manager.files_store import files_store
from socket_server.messages.socket_message import error_message, file_download_message, file_upload_message, json_message, socket_message
from socket_server.message_verifier import message_verifier
from model.message import message as chat_message
from store.message_store import message_store
from socket_server.connection_pool import connection_pool

#This class is responsible for carrying out the commands of 
#the user.
# TODO switch to command pattern
class message_resolver:

    def __init__(self, msg: socket_message, conn: connection = None, queue: Queue = None):
        self.msg = msg
        self.command_type = ''
        self.payload = {}
        self.is_processed = False
        self.conn = conn
        self.queue = queue

    def process(self):
        if self.is_processed:
            return None
        

        v = message_verifier.verify_message(self.msg)
        if v:
            self.is_processed = True
            return self._resolve_message()
        else:
            return error_message('Incorrect Message Syntax')
    

        
    def _resolve_message(self):
        r = self.msg.header[HEADER_REQUEST]

        if r == REQUEST_UPLOAD_FILE:
            return self._upload_file()
        
        if r == REQUEST_MESSAGE_SEND:
            return self._send_message()

        if r == REQUEST_DOWNLOAD_FILE:
            return self._download_file()

        if r == REQUEST_POLL_MESSAGES:
            return self._poll_messages()

        if r == REQUEST_MESSAGES_RECEIVED:
            return self._messages_received()

    def _send_message(self):
        msg: json_message = self.msg
        content = msg.content
        chat_msg = chat_message(
            id= None,
            from_id= authenticator.get_instance().get_user_id(msg[HEADER_TOKEN]),
            to_id=content[BODY_TO_ID],
            media_id=content[BODY_MEDIA_ID],
            message_text=content[BODY_MESSAGE_TEXT],
            time=datetime.now()
        )
        
        # store message
        result = None
        try:
            result = message_store.get_instance().store_message(chat_msg)
        except Exception as e:
            return error_message(str(e))

        assert(isinstance(result, str))
        

        result_msg = json_message(
                message_type = REQUEST_MESSAGE_STORED, 
                content = {BODY_MESSAGE_ID: result},
                header={}
            )
        print("resulting msg: ", result_msg)
        
        self._notify_user_of_new_messages(chat_msg.to_id)

        return result_msg

    
    def _upload_file(self):
        msg: file_upload_message = self.msg
        token = self.msg.header[HEADER_TOKEN]
        type = self.msg.header[HEADER_FILE_EXTENSION]
        file_path = msg.file_path

        sender_id = authenticator.get_instance().get_user_id(token)
        if not sender_id:
            print("Token invalid")
            return error_message('Invalid token')

        date = datetime.today().ctime().replace(':', '-')
        try:
            result = files_store.upload_file(sender_id, f'CHATAPP-{sender_id}-{date}', file_path, type)
            return json_message(REQUEST_FILE_UPLOADED, {BODY_MEDIA_ID: result}, {})        
        except Exception as e:
            print("SOme exception occured ")
            return error_message(f"There was an error while uploading the file: {str(e)}")


    # TODO this is not the best way to send a file especially for big ones
    # find a better way...
    def _download_file(self):
        token = self.msg.header[HEADER_TOKEN]
        if not authenticator.get_instance().get_user_id(token):
            return error_message('Invalid token')
        
        content = self.msg.content
        media_id = content[BODY_MEDIA_ID]

        f = files_store.get_file_details(media_id)
        if not f:
            return error_message('This files does not exist')

        user_id = f.file_name.split('-')[1]

        path = files_store.get_file_path(user_id, f.file_name)
        return file_download_message(f, path)

 
    def _poll_messages(self):
        """
        Return all messages to the user and 
        register them to receive further messages
        """

        header = self.msg.header
        token = header[HEADER_TOKEN]
        user_id = authenticator.get_instance().get_user_id(token)
        if not user_id:
            return error_message('Invalid token')

        # add to the connection pool
        self.conn.user_id = user_id
        pool = connection_pool.get_instance()
        pool.add_connection(self.conn, user_id)

        # send messages
        messages = message_store.get_instance().get_messages_to(user_id)
        for i in range(0, len(messages)):
            msg = messages[i]
            msg['id'] = str(msg['_id'])
            del msg['_id']
            messages[i] = msg

        result_message = json_message(REQUEST_MESSAGE_RECEIVE, {BODY_MESSAGES: messages}, {})

        msgs_updates = message_store.get_instance().get_message_updates_to(user_id)
        if msgs_updates != None:
            result_message.add_item(BODY_RECEIVED_MESSAGES, msgs_updates.received_messages)
            result_message.add_item(BODY_READ_MESSAGES, msgs_updates.read_messages)

        return result_message

    def _messages_received(self):
        token = self.msg[HEADER_TOKEN]
        user_id = authenticator.get_instance().get_user_id(token)
        if not user_id:
            return error_message("Invalid Token")

        msg_content = json.loads(self.msg.content.decode('utf-8'))
        msg_ids = msg_content[BODY_MESSAGES_IDS]
        to_id = msg_content[BODY_USER_ID]

        for id in msg_ids:
            try:
                message_store.get_instance().add_received_message(to_id, id)
            except BaseException as e: # message is not found or something
                print(str(e))

        self._notify_user_of_new_messages(to_id)
        
    def _messages_read(self):
        token = self.msg[HEADER_TOKEN]
        user_id = authenticator.get_instance().get_user_id(token)
        if not user_id:
            return error_message("Invalid Token")

        msg_content = json.loads(self.msg.content.decode('utf-8'))
        msg_ids = msg_content[BODY_MESSAGES_IDS]
        to_id = msg_content[BODY_USER_ID]

        for id in msg_ids:
            try:
                message_store.get_instance().add_read_message(to_id, id)
            except: # message is not found or something
                continue

        self._notify_user_of_new_messages(to_id)
    

    def _notify_user_of_new_messages(self, user_id: str):
        pool = connection_pool.get_instance()
        conn: connection = pool.get_connection(user_id)
        
        # user is offline
        if conn == None:
            return

        notification_msg = json_message(message_type=REQUEST_PENDING_MESSAGES, content={}, header = {})
        conn.send_message(notification_msg)
