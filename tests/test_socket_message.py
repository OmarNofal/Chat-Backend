import struct
import unittest
from model.file import file
from socket_server.messages.socket_message import file_download_message, socket_message, json_message
import io
import json
from socket_server.stream_utils import chain_streams
from utils.constants import HEADER_CONTENT_LENGTH, HEADER_FILE_EXTENSION



class TestSocketMessage(unittest.TestCase):
    

    def test_get_proto_and_header_bytes(self):

        class subclass(socket_message):
            def get_message_stream(self) -> io.BufferedIOBase:
                return super().get_message_stream()
        
        test_header = {'o': '1'}
        print(len(json.dumps(test_header).encode('utf-8')))

        s = subclass(test_header)
        bytesio = s._get_proto_and_header_bytesio()

        header_bytes = bytesio.read()
        protoheader = header_bytes[:2]
        header = json.loads(header_bytes[2:].decode('utf-8'))

        self.assertEqual(protoheader, b'\x00\x0a', 'Protoheader is not correct')
        self.assertEqual(header, test_header, 'Header is not correct')

    def test_incorrect_content_type_raises_error(self):
        
        class subclass(json_message):
            pass

        self.assertRaises(TypeError, subclass.__init__, '123', '123')
        
            
    def test_chain_streams_works(self):

        s1 = io.BytesIO(b'omar')
        s2 = io.BytesIO(b'walid')

        s3 = chain_streams([s1, s2])
        self.assertEquals(s3.read().decode("utf-8"),"omarwalid", 'the two strings do not match')


    def test_file_download_message(self):
        f = file(file_extension='txt')
        file_location = "tests/test_file.txt"
        f_download_message = file_download_message(f, file_location)
        msg_bytes = f_download_message.get_message_stream().read()

        proto = struct.unpack('>H',msg_bytes[0:2])[0]
        header = json.loads(  msg_bytes[2:(proto + 2)].decode('utf-8') )
        cont_length = header[HEADER_CONTENT_LENGTH]
        file_text = msg_bytes[proto + 2 : cont_length + proto + 2].decode('utf-8')

        self.assertEquals(header[HEADER_FILE_EXTENSION], f.file_extension)
        self.assertEquals(file_text, 'omarwalid')






if __name__ == '__main__':
    unittest.main()