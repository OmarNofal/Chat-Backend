import json
import os
import pathlib
import selectors
import socket
import struct
import uuid

from utils.constants import HEADER_CONTENT_LENGTH, HEADER_REQUEST, REQUEST_UPLOAD_FILE

from .messages.socket_message import socket_message
from .messages.socket_message import json_message
from .messages.socket_message import file_upload_message

"""
Steps to read a message

1- Read 2 bytes to retreive the protoheader (N)
2- Read untill N bytes are availabe in the buffer to read header
3- Retreive `content-length` from header to read content
4- Check request field in the header
    4.1- if it is an upload file request then create a file_upload_message object
    4.2- else: then it is a json_message object
"""

UPLOADED_FILES_DIR = './TempUploadedFiles'


class socket_reader:
    """ Reads data from socket and encodes the 
    data in Message objects """
    def __init__(self, sock: socket.socket):
        self.sock: socket.socket = sock
        self.buffer = b''
        self.header_len = None
        self.header_read = False
        self.messages: list[socket_message] = []
        self.is_closed = False
        self.uploaded_file = None # this will be None if the user is not uploading a file, it will be a file stream otherwise


    def process_events(self):
        self._read()
        
    def _read(self):
        self._read_to_buffer()
        if not self.header_len:
            self._read_protoheader()
        
        if self.header_len is not None:
            if not self.header_read:
                self._read_header()
        if self.header_read:
            self._read_content()

    def _read_to_buffer(self):
        try:
            data = self.sock.recv(4096)
        except Exception as e:
            self.is_closed = True
        else:
            if data:
                self.buffer += data
            else:
                print("Peer closed connection")
                self.is_closed = True


    def _read_protoheader(self):
        if len(self.buffer) >= 2:
            self.header_len = struct.unpack(">H", self.buffer[:2])[0]
            self.buffer = self.buffer[2:]

    def _read_header(self):
        header_len = self.header_len
        if len(self.buffer) >= header_len:
            header = self.buffer[:header_len]
            header_json = json.loads(header.decode('utf-8'))

            if HEADER_CONTENT_LENGTH not in header_json:
                print('Header formatted incorrectly (content-length not found)')
                self.is_closed = True
                return
            
            if HEADER_REQUEST not in header_json:
                print('Header not formatted correctly missing request field')
                self.is_closed = True
                return

            request = header_json[HEADER_REQUEST]
            if request == REQUEST_UPLOAD_FILE:
                # user is uploading a file
                home_dir = pathlib.Path.home()
                home_dir.joinpath(UPLOADED_FILES_DIR).mkdir(exist_ok=True)
                path = str(home_dir.joinpath(UPLOADED_FILES_DIR).joinpath(str(uuid.uuid4())))
                self.uploaded_file = open(path, 'wb')

            self.content_length = header_json["content-length"]
            self.buffer = self.buffer[header_len:]

            self.header = header_json
            self.header_read = True
    
    def _read_content(self):

        if self.uploaded_file is not None: # we are uploading a file
            num_bytes_to_read = min(self.content_length, len(self.buffer))
            bytes_read = self.buffer[:num_bytes_to_read]
            self.buffer = self.buffer[num_bytes_to_read:]
            self.content_length -= num_bytes_to_read
            self.uploaded_file.write(bytes_read)

        elif len(self.buffer) >= self.content_length:
            self.content = self.buffer[:self.content_length]
            self.buffer = self.buffer[self.content_length:]
            self.content_length = 0

        if self.content_length is None or self.content_length == 0: # whole message was read, now let's create messaege object
            msg: socket_message = None
            header_dict = self.header
            if self.uploaded_file is not None:
                file_path = self.uploaded_file.name
                msg = file_upload_message(header_dict, file_path)
                self.messages.append(msg)
            else:
                content_dict = json.loads(self.content)
                msg = json_message(header_dict[HEADER_REQUEST], content_dict, header_dict)
                self.messages.append(msg)

            # reset reader to be able to read a new message
            self.header_len = None
            self.header_read = False
            self.header = None
            self.content_length = None
            if (self.uploaded_file != None):
                self.uploaded_file.close()
    

    def pop_message(self) -> socket_message:
        msg = self.messages.pop(0)
        return msg

    def has_messages(self):
        return len(self.messages) > 0
