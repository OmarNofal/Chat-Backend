import unittest
from unittest.mock import Mock
from socket_server.messages.socket_message import *
from socket_server.socket_writer import socket_writer



class TestSocketWriter(unittest.TestCase):

    def test_writer_sends_one_message(self):

        msg = json_message(REQUEST_DOWNLOAD_FILE, {'h': '1'}, {'o': '2'})
        bytes = msg.get_message_stream().read()

        socket_mock = Mock()
        socket_mock.send.return_value = 4096

        writer = socket_writer(socket_mock)
        writer.enqueue_message(msg)

        while writer.has_messages():
            writer.process_events()
        
        args = socket_mock.send.call_args_list
        sent_bytes = b''
        for arg in args:
            sent_bytes += arg[0][0]
            
        
        self.assertEqual(sent_bytes, bytes, 'bytes sent are different from message bytes')

    def test_writer_send_multiple_messages(self):
        msgs = [
            json_message(REQUEST_UPLOAD_FILE),
            json_message(REQUEST_DOWNLOAD_FILE),
            json_message(REQUEST_MESSAGE_DELETE)
        ]

        test_bytes = b''
        for m in msgs:
            test_bytes += m.get_message_stream().read()

        socket_mock = Mock()
        socket_mock.send.return_value = 4096

        writer = socket_writer(socket_mock)
        for m in msgs: writer.enqueue_message(m)

        while writer.has_messages():
            writer.process_events()
        
        sent_bytes = b''
        for arg in socket_mock.send.call_args_list:
            sent_bytes += arg[0][0]
        
        self.assertEquals(sent_bytes, test_bytes)

    
    def test_send_download_file_message(self):
        file_location = 'tests/test_file.txt'
        msg = file_download_message(file(file_extension='txt'), file_location)

        test_bytes = msg.get_message_stream().read()

        socket_mock = Mock()
        socket_mock.send.return_value = 5

        writer = socket_writer(socket_mock)
        writer.enqueue_message(msg)

        while writer.has_messages():
            writer.process_events()
        
        socket_mock.send.assert_called_with(b'walid') # last 5 bytes sent from the file



if __name__ == '__main__':
    unittest.main()