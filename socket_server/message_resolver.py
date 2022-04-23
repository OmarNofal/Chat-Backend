

import base64
from datetime import datetime
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
#the user TODO switch to command pattern
class message_resolver:

    def __init__(self, msg: socket_message):
        self.msg = msg
        self.command_type = ''
        self.payload = {}
        self.is_processed = False


    def process(self):
        if self.is_processed:
            return None
        

        v = message_verifier.verify_message(self.msg)
        if v:
            self._parse_message()
            self.is_processed = True
            return self._resolve_message()
        else:
            return {
                'result': 'error',
                'message': 'incorrect message syntax'
            }
    

        
    def _resolve_message(self):
        r = self.command_type

        if r == REQUEST_UPLOAD_FILE:
            return self._upload_file()
        
        if r == REQUEST_MESSAGE_SEND:
            return self._send_message()

        if r == REQUEST_DOWNLOAD_FILE:
            return self._download_file()

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
        
        msg = socket_message(
            header = {
                HEADER_REQUEST: REQUEST_PENDING_MESSAGES
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
  

    def _parse_message(self):
        self.command_type = self.msg['request'].lower()
        self.content = self.msg.content

    