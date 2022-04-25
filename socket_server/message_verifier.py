import json

from .socket_message import socket_message as message
from utils.constants import *

class message_verifier:


    valid_requests = [
        REQUEST_MESSAGE_SEND, 
        REQUEST_UPLOAD_FILE, 
        REQUEST_MESSAGE_DELETE,
        REQUEST_MESSAGES_READ,
        REQUEST_POLL_MESSAGES
    ]

    def __init__(self) -> None:
        pass

    def verify_message(msg: message):
        header = msg.header

        correct_header = message_verifier.verify_header(header)
        
        if not correct_header:
            return False

        request = header[HEADER_REQUEST]

        if request == REQUEST_MESSAGE_SEND:
            return message_verifier.verify_send_message(msg)
        
        if request == REQUEST_MESSAGE_DELETE:
            return message_verifier.verify_delete_message(msg)

        if request == REQUEST_UPLOAD_FILE:
            return message_verifier.verify_upload_file(msg)

        if request == REQUEST_MESSAGES_READ:
            return message_verifier.verify_messages_read(msg)

        if request == REQUEST_DOWNLOAD_FILE:
            return message_verifier.verify_download_file(msg)
        
        if request == REQUEST_POLL_MESSAGES:
            return True # no body in this type so no need to check for it

        return False

    def verify_header(header: dict):
        if not {HEADER_REQUEST, HEADER_TOKEN} <= header.keys():
            return False
        return True

    def verify_send_message(msg: message):
        try:
            json_string = msg.content.decode('utf-8')
            m = json.loads(json_string)

            if not BODY_TO_ID in m:
                return False

            return True
        except Exception as e:
            return False

    
    def verify_delete_message(msg: message):
        try:
            json_string = msg.content.decode('utf-8')
            m = json.loads(json_string)

            if not BODY_MESSAGE_ID in m:
                return False

            return True
        except Exception as e:
            return False

    def verify_upload_file(msg: message):
        try:
            header = msg.header
            print("checkin upload file")
            if not {HEADER_FILE_TYPE} <= header.keys():
                return False

            return True
        except Exception as e:
            return False

    def verify_messages_read(msg: message):
        try:
            json_string = msg.content.decode('utf-8')
            m = json.loads(json_string)

            if not BODY_TO_ID in m:
                return False

            return True
        except Exception as e:
            return False

    def verify_download_file(msg: message):
        try:
            json_string = msg.content.decode('utf-8')
            m = json.loads(json_string)

            if not BODY_MEDIA_ID in m:
                return False
            
            return True
        except Exception as e:
            return False