import os
import unittest

from isort import stream
from socket_server.messages.socket_message import file_upload_message, json_message, socket_message
from socket_server.socket_reader import socket_reader
from utils.constants import HEADER_CONTENT_LENGTH, HEADER_REQUEST, REQUEST_DOWNLOAD_FILE, REQUEST_UPLOAD_FILE
from unittest.mock import Mock
import io
from socket_server.stream_utils import chain_streams


class mock_socket:

    def __init__(self, data_stream) -> None:
        self.stream: io.BufferedReader = data_stream
    
    def recv(self, size: int) -> bytes:
        return self.stream.read(size)

class test_msg(socket_message):
            def __init__(self, header: dict, file: io.BufferedReader) -> None:
                super().__init__(header)
                self.header[HEADER_REQUEST] = REQUEST_UPLOAD_FILE
                self.file = file
            
            def get_message_stream(self) -> io.BufferedReader:
                self.header[HEADER_CONTENT_LENGTH] = os.path.getsize(self.file.name)
                header = self._get_proto_and_header_bytesio()
                return chain_streams([header, self.file])

class TestSocketReader(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        print('test ran')

    def test_reads_one_json_message(self):
        msg = json_message(REQUEST_DOWNLOAD_FILE, content = {'o': '1'}, header = {'x': '2'})
        sock = Mock()
        sock.recv.return_value = msg.get_message_stream().read()
        reader = socket_reader(sock)

        while not reader.has_messages():
            reader.process_events()
        
        read_message = reader.pop_message()
        
        self.assertEqual(read_message.get_message_stream().read(), msg.get_message_stream().read())


    def test_reads_one_file_message(self):

        f = open('tests/test_image.jpg', 'rb')
        tst_msg = test_msg({}, file = f)
        sock = mock_socket(tst_msg.get_message_stream())
        reader = socket_reader(sock)

        while not reader.has_messages():
            reader.process_events()
        
        msg = reader.pop_message()

        self.assertIsInstance(msg, file_upload_message)
        self.assertIsNotNone(msg.file_path)


    def test_reads_multiple_messages(self):
        msg_1 = json_message(REQUEST_DOWNLOAD_FILE, header={'o': '1'})
        f = open('tests/test_image.jpg', 'rb')
        msg_2 = test_msg({}, file = f)
        sock = mock_socket(chain_streams([msg_1.get_message_stream(), msg_2.get_message_stream()]))

        reader = socket_reader(sock)
        while len(reader.messages) < 2:
            reader.process_events()
        
        m_1 = reader.pop_message()
        self.assertEqual(m_1.get_message_stream().read(), msg_1.get_message_stream().read())

        m_2 = reader.pop_message()
        self.assertIsInstance(m_2, file_upload_message)
        self.assertIsNotNone(m_2.file_path)




