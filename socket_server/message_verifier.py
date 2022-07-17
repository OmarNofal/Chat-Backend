import json

from .messages.socket_message import socket_message as message
from utils.constants import *

class message_verifier:
    """
    This class contains a static method `verify_message` whose function is to 
    check that the syntax of the message is correct
    """

    valid_requests = [
        REQUEST_MESSAGE_SEND, 
        REQUEST_UPLOAD_FILE, 
        REQUEST_MESSAGE_DELETE,
        REQUEST_MESSAGES_READ,
        REQUEST_POLL_MESSAGES,
        REQUEST_MESSAGES_RECEIVED,
        REQUEST_MESSAGES_READ
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

        if request == REQUEST_MESSAGES_RECEIVED:
            return message_verifier.verify_messages_received(msg)

        if request == REQUEST_MESSAGES_READ:
            return message_verifier.verify_messages_read(msg)

        return False

    def verify_header(header: dict):
        if not {HEADER_REQUEST, HEADER_TOKEN} <= header.keys():
            return False
        return True

    def verify_send_message(msg: message):
        try:
            m = msg.content

            if not BODY_TO_ID in m:
                return False

            return True
        except:
            return False

    
    def verify_delete_message(msg: message):
        try:
            m = msg.content

            if not BODY_MESSAGE_ID in m:
                return False

            return True
        except:
            return False

    def verify_upload_file(msg: message):
        try:
            header = msg.header
            if not {HEADER_FILE_EXTENSION} <= header.keys():
                return False

            return True
        except:
            return False

    # def verify_messages_read(msg: message):
    #     try:
            
    #         m = msg.content

    #         if not BODY_TO_ID in m:
    #             return False

    #         return True
    #     except:
    #         return False

    def verify_download_file(msg: message):
        try:
            m = msg.content

            if not BODY_MEDIA_ID in m:
                return False
            
            return True
        except:
            return False

    def verify_messages_received(msg: message):
        try:
            content = msg.content
            if not BODY_MESSAGES_IDS in content or not isinstance(content[BODY_MESSAGES_IDS], list):
                return False
            if not BODY_USER_ID in content:
                return False
            return True
        except:
            return False

    def verify_messages_read(msg: message):
        try:
            print('verifiying messages read')
            content = msg.content
            print(content, end='\n\n')
            if not BODY_MESSAGES_IDS in content or not isinstance(content[BODY_MESSAGES_IDS], list):
                return False
            if not BODY_USER_ID in content:
                return False
            return True
        except:
            return False