import json
from .socket_message import socket_message as message


class message_verifier:


    valid_requests = ['send_message', 'upload_file', 'delete_message', 'messages_read']

    def __init__(self) -> None:
        pass

    def verify_message(msg: message):
        header = msg.header
        content = msg.content

        if not {'request', 'token'} <= header.keys():
            return False
        
        request = header['request']

        if not request in message_verifier.valid_requests:
            return False

        if request == 'send_message':
            return message_verifier.verify_send_message(msg)
        
        if request == 'delete_message':
            return message_verifier.verify_delete_message(msg)

        if request == 'upload_file':
            return message_verifier.verify_upload_file(msg)

        if request == 'messages_read':
            return message_verifier.verify_messages_read(msg)

    def verify_send_message(msg: message):
        try:
            json_string = msg.content.decode('utf-8')
            m = json.loads(json_string)

            if not 'to_id' in m:
                return False

            return True
        except Exception as e:
            return False

    
    def verify_delete_message(msg: message):
        try:
            json_string = msg.content.decode('utf-8')
            m = json.loads(json_string)

            if not 'message_id' in m:
                return False

            return True
        except Exception as e:
            return False

    def verify_upload_file(msg: message):
        try:
            header = msg.header
            print("checkin upload file")
            if not {'type'} <= header.keys():
                return False

            return True
        except Exception as e:
            return False

    def verify_messages_read(msg: message):
        try:
            json_string = msg.content.decode('utf-8')
            m = json.loads(json_string)

            if not 'to_id' in m:
                return False

            return True
        except Exception as e:
            return False