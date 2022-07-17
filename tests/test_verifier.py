from socket import socket
import unittest
import json

from socket_server.message_verifier import message_verifier as verifier
from socket_server.messages.socket_message import file_upload_message, socket_message, json_message
from utils.constants import *



class TestMessageVerifier(unittest.TestCase):
   

    def test_verify_headers_correct(self):
        correct_msg = json_message(header = {HEADER_REQUEST: REQUEST_DOWNLOAD_FILE, HEADER_TOKEN: '123'})
        wrong_msg2 = json_message(header = {HEADER_REQUEST: REQUEST_MESSAGE_SEND, HEADER_FILE_TYPE: 'mp4'}) # no token

        self.assertTrue(verifier.verify_header(correct_msg.header))
        self.assertFalse(verifier.verify_header(wrong_msg2.header))


    def test_verify_send_message(self):
        correct_msg = json_message(
            message_type=REQUEST_MESSAGE_SEND,
            header={HEADER_TOKEN: '123'},
            content={BODY_TO_ID: '0129', BODY_MEDIA_ID: '123'}
            )
        wrong_message = json_message(
            header={HEADER_REQUEST: REQUEST_MESSAGE_SEND, HEADER_TOKEN: '123'},
            content={BODY_MEDIA_ID: '0129'} # no media id 
            )
        wrong_message2 = json_message(
            header={HEADER_REQUEST: REQUEST_MESSAGE_SEND}, # no token
            content={BODY_TO_ID: '0129'}
            )

        self.assertTrue(verifier.verify_message(correct_msg))
        self.assertFalse(verifier.verify_message(wrong_message))
        self.assertFalse(verifier.verify_message(wrong_message2))


    def test_verify_upload_file(self):
        correct_msg = file_upload_message(
            header={HEADER_REQUEST: REQUEST_UPLOAD_FILE, HEADER_TOKEN: '123', HEADER_FILE_TYPE: 'mp4'}
            )
        wrong_message = file_upload_message(
            header={HEADER_REQUEST: REQUEST_UPLOAD_FILE, HEADER_TOKEN: '123'} # no FILE_TYPE in the header
            )

        self.assertTrue(verifier.verify_message(correct_msg))
        self.assertFalse(verifier.verify_message(wrong_message))


    def test_verify_delete_message(self):
        correct_msg = socket_message(
            header={HEADER_REQUEST: REQUEST_MESSAGE_DELETE, HEADER_TOKEN: '123'},
            content=json.dumps({BODY_MESSAGE_ID: '0129'}).encode('utf-8')
            )
        wrong_message = socket_message(
            header={HEADER_REQUEST: REQUEST_MESSAGE_DELETE, HEADER_TOKEN: '123'},
            content=json.dumps({BODY_MEDIA_ID: '0129'}).encode('utf-8') # no message id
            )
        wrong_message2 = socket_message(
            header={HEADER_REQUEST: REQUEST_MESSAGE_DELETE, HEADER_TOKEN: '123'},
            content=f'{BODY_MESSAGE_ID}: "12031"'.encode('utf-8') # invalid json
            )

        self.assertTrue(verifier.verify_message(correct_msg))
        self.assertFalse(verifier.verify_message(wrong_message))
        self.assertFalse(verifier.verify_message(wrong_message2))


    def test_verify_messages_read(self):
        correct_msg = socket_message(
            header={HEADER_REQUEST: REQUEST_MESSAGES_READ, HEADER_TOKEN: '123'},
            content=json.dumps({BODY_TO_ID: '0129'}).encode('utf-8')
            )
        wrong_message = socket_message(
            header={HEADER_REQUEST: REQUEST_MESSAGES_READ, HEADER_TOKEN: '123'},
            content=json.dumps({}).encode('utf-8') # no user id
            )
        wrong_message2 = socket_message(
            header={HEADER_REQUEST: REQUEST_MESSAGES_READ, HEADER_TOKEN: '123'},
            content=f'{BODY_MESSAGE_ID}: "12031"'.encode('utf-8') # invalid json
            )

        self.assertTrue(verifier.verify_message(correct_msg))
        self.assertFalse(verifier.verify_message(wrong_message))
        self.assertFalse(verifier.verify_message(wrong_message2))

    def test_verify_download_file(self):
        correct_msg = socket_message(
            header={HEADER_REQUEST: REQUEST_DOWNLOAD_FILE, HEADER_TOKEN: '123'},
            content=json.dumps({BODY_MEDIA_ID: '0129'}).encode('utf-8')
            )
        wrong_message = socket_message(
            header={HEADER_REQUEST: REQUEST_DOWNLOAD_FILE, HEADER_TOKEN: '123'},
            content=json.dumps({}).encode('utf-8') # no media_id
            )

        self.assertTrue(verifier.verify_message(correct_msg))
        self.assertFalse(verifier.verify_message(wrong_message))

    # def test_verify_messages_receieved(self):
    #     correct_msg = socket_message(
    #         header={HEADER_REQUEST: REQUEST_MESSAGES_RECEIVED, HEADER_TOKEN: '123'},
    #         content=json.dumps({BODY_MESSAGES_IDS: ['123', '123', '123']}).encode('utf-8')
    #         )
    #     wrong_message = socket_message(
    #         header={HEADER_REQUEST: REQUEST_MESSAGES_READ, HEADER_TOKEN: '123'},
    #         content=json.dumps({BODY_MESSAGES_IDS: {}}).encode('utf-8')
    #         )
        
    #     self.assertTrue(verifier.verify_message(correct_msg))
    #     self.assertFalse(verifier.verify_message(wrong_message))


if __name__ == "__main__":
    unittest.main()