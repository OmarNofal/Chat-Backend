

import base64
from datetime import datetime
from queue import Queue
from socket import socket
import json


from socket_server.connection import connection
from utils.constants import *
from auth.authenticator import authenticator
from files_manager.files_store import files_store
from socket_server.socket_message import socket_message
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
            return {
                'result': 'error',
                'message': 'incorrect message syntax'
            }
    

        
    def _resolve_message(self):
        r = self.msg[HEADER_REQUEST]

        if r == REQUEST_UPLOAD_FILE:
            return self._upload_file()
        
        if r == REQUEST_MESSAGE_SEND:
            return self._send_message()

        if r == REQUEST_DOWNLOAD_FILE:
            return self._download_file()

        if r == REQUEST_POLL_MESSAGES:
            return self._poll_messages()

    def _send_message(self):
        msg = self.msg
        content = json.loads(msg.content.decode('utf-8'))
        chat_msg = chat_message(
            id= None,
            from_id= authenticator.get_instance().get_user_id(msg[HEADER_TOKEN]),
            to_id=content[BODY_TO_ID],
            media_id=content[BODY_MEDIA_ID],
            message_text=content[BODY_MESSAGE_TEXT]
        )
        
        # store message
        result = message_store.get_instance().store_message(chat_msg)
        if result['result'] == 'error':
            return result # msg not inserted 

        # TODO move message notification to appropriate class (seperation of concerns)
        # notify the reciever of the message if they are connected
        pool = connection_pool.get_instance()
        user_connections = pool.get_all_connections(content[BODY_TO_ID])
        conn: connection = user_connections[0] if user_connections != None else None
        # user is offline
        if conn == None:
            return result
        print(conn.user_id)
        print(conn.is_closed)
        msg = socket_message(
            header = {
                HEADER_REQUEST: REQUEST_PENDING_MESSAGES,
                HEADER_CONTENT_LENGTH: 0
            }
        )
        conn.send_message(msg)

        return result

    
    def _upload_file(self):
        token = self.msg.header[HEADER_TOKEN]
        type = self.msg.header[HEADER_FILE_TYPE]
        content = self.msg.content

        sender_id = authenticator.get_instance().get_user_id(token)
        if not sender_id:
            return

        date = datetime.today().ctime().replace(':', '-')
        return files_store.upload_file(
            sender_id,
            f'CHATAPP-{sender_id}-{date}',
            content,
            type
            )


    # TODO this is not the best way to send a file especially for big ones
    # find a better way...
    def _download_file(self):
        token = self.msg.header[HEADER_TOKEN]
        if not authenticator.get_instance().get_user_id(token):
            return {'result': 'error', 'msg': 'invalid token'}
        
        content = self.msg.content.decode('utf-8')
        j = json.loads(content)
        media_id = j[BODY_MEDIA_ID]

        f = files_store.get_file_details(media_id)
        if not f:
            return {'result': 'error', 'message': 'This files does not exist'}
        
        
        user_id = f.file_name.split('-')[1]

        path = files_store.get_file_path(user_id, f.file_name)
        
        f_bytes = b''
        with open(path,'rb') as fi:
            f_bytes = fi.read()
        
        result = f.as_dict()
        result['file_bytes'] = base64.b64encode(f_bytes).decode('ascii')
        return result

  
    def _poll_messages(self):
        """
        Return all messages to the user and 
        register them to receive further messages
        """

        header = self.msg.header
        token = header[HEADER_TOKEN]
        user_id = authenticator.get_instance().get_user_id(token)
        if not user_id:
            return {'result': 'error', 'message': 'invalid token'}

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

        return messages  