# import selectors
# import socket
# import unittest
# import json

# from db.database import app_database as database
# from socket_server.connection import connection
# from socket_server.connection_pool import connection_pool
# from socket_server.messages.socket_message import socket_message
# from socket_server.message_resolver import message_resolver
# from utils.constants import *


# class TestMessageResolver(unittest.TestCase): 
    
#     def test_message_sent(self):
#         msg = socket_message(
#             header={HEADER_REQUEST: REQUEST_MESSAGE_SEND, HEADER_TOKEN: '6c3b9a50-561a-4acf-9fa7-51d949795d91'},
#             content=json.dumps({
#                 BODY_MESSAGE_TEXT: "Test message",
#                 BODY_TO_ID: '61fad0c133eae449d8d6c01a',
#                 BODY_MEDIA_ID: ''
#             }).encode('utf-8')
#         )

#         resolver = message_resolver(msg)
#         self.assertEqual(resolver.process()['result'], 'success')


#     def test_notification_sent(self):
#         msg = socket_message(
#             header={HEADER_REQUEST: REQUEST_MESSAGE_SEND, HEADER_TOKEN: '6c3b9a50-561a-4acf-9fa7-51d949795d91'},
#             content=json.dumps({
#                 BODY_MESSAGE_TEXT: "Test message",
#                 BODY_TO_ID: '61fad0c133eae449d8d6c01a',
#                 BODY_MEDIA_ID: ''
#             }).encode('utf-8')
#         )

#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         selector = selectors.DefaultSelector()
#         selector.register(sock, selectors.EVENT_READ, None)
#         conn = connection(selector, sock)
#         pool = connection_pool.get_instance()

#         pool.add_connection(conn, '61fad0c133eae449d8d6c01a')
#         resolver = message_resolver(msg)

#         resolver.process()
        
#         self.assertEqual(REQUEST_PENDING_MESSAGES, conn.writer.messages[0][HEADER_REQUEST])
        


# if __name__ == "__main__" :
#     unittest.main()