

from datetime import datetime
from socket import socket
from auth.authenticator import authenticator
from files_manager.files_store import files_store
from socket_server.socket_message import socket_message
from socket_server.message_verifier import message_verifier
from model.message import message as chat_message
import json

from store.message_store import message_store

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
        msg = self.msg
        r = self.command_type
        c = self.content

        if r == 'upload_file':
            return self._upload_file()
        
        if r == 'send_message':
            return self._send_message()

    def _send_message(self):
        msg = self.msg
        content = json.loads(msg.content.decode('utf-8'))
        chat_msg = chat_message(
            id= None,
            from_id= authenticator.get_instance().get_user_id(msg['token']),
            to_id=content['to_id'],
            media_id=content['media_id'],
            message_text=content['message_text']
        )
       
        return message_store.get_instance().store_message(chat_msg)
       
        #TODO notify the reciever of the message if they are connected
        
    def _upload_file(self):
        token = self.msg.header['token']
        type = self.msg.header['type']
        content = self.msg.content

        sender_id = authenticator.get_instance().get_user_id(token)
        date = datetime.today().ctime().replace(':', '-')
        return files_store.upload_file(
            sender_id,
            f'CHATAPP-{sender_id}-{date}',
            content,
            type
            )

    def _parse_message(self):
        self.command_type = self.msg['request'].lower()
        self.content = self.msg.content

    