"""
This module contains the messages types that are communicated between the server and the client
All messages contain a header which is described in `socket_message` class.
"""

from abc import abstractmethod, ABC
import json
import os
import struct
import io

from model.file import file
from utils.constants import *
from socket_server.stream_utils import chain_streams

class socket_message(ABC):
    """
    Abstract class that represents a message sent between the client and the server.\n
    Each message has a header and messages follow this form

    2 bytes (BE): Protoheader tells us how long the header is (N)
    N bytes: This is the actual header (json) encoded in utf-8 format
    Additionally the header contains a 'content-length' field which 
    tells us how many bytes to read after the header to get the actual content
    """


    def __init__(self,
    header: dict = {},
    ) -> None:
        self.h = header


    @abstractmethod
    def get_message_stream(self) -> io.BufferedReader:
        """
        This messages returns a buffered io representing the contents of this message.
        Note that this method returns a new io 
        """
        pass

    def _get_proto_and_header_bytesio(self) -> io.BytesIO:
        header_bytes = json.dumps(self.header).encode('utf-8')
        header_length = len(header_bytes)
        proto_bytes = struct.pack('>H', header_length)
        all_bytes = proto_bytes + header_bytes
        return io.BytesIO(all_bytes)

    def __getitem__(self, key):
        return self.h[key]
    
    def __setitem__(self, key, value):
        self.h[key] = value

    def __delitem__(self, key):
        del self.h[key]

    @property
    def header(self) -> dict:
        return self.h  


class json_message(socket_message):
    """
    Class that represents a message where the content is of type json
    """

    def __init__(self, message_type: str = "", content: dict = {}, header: dict = {}) -> None:
        super().__init__(header)
        self.header[HEADER_REQUEST] = message_type
        if (not isinstance(content, dict)):
            raise TypeError("Content must be a dict object")
        self.content = content
        
    def get_message_stream(self) -> io.BufferedReader:
        content_bytes = json.dumps(self.content).encode('utf-8')
        self.header['content-length'] = len(content_bytes)
        header_bytesio = self._get_proto_and_header_bytesio()
        content_bytesio = io.BytesIO(content_bytes)
        return chain_streams([header_bytesio, content_bytesio])



class file_download_message(socket_message):
    """
    Class that represents a message where the content is a file to be downloaded (given to the client)
    """
    def __init__(self, f: file, file_location: str) -> None:
        header = {HEADER_REQUEST: REQUEST_DOWNLOAD_FILE}
        super().__init__(header)
        self.file_location = file_location
        self.f = f

    
    def get_message_stream(self) -> io.BufferedReader:
        f_stream = open(self.file_location, 'rb')
        self.header[HEADER_CONTENT_LENGTH] = os.path.getsize(self.file_location)
        self.header[HEADER_FILE_EXTENSION] = self.f.file_extension
        header_stream = self._get_proto_and_header_bytesio()
        return chain_streams([header_stream, f_stream]) 



class file_upload_message(socket_message):
    """
    Class that represents a message where the user is uploading a file to the server.
    When the user uploads a file, the class `socket_reader` writes the files contents
    to the file system in temp_uploads directory.
    This class only contains the headers and the file path
    """
    def __init__(self, header: dict = {}, file_path: str = '') -> None:
        if header[HEADER_REQUEST] != REQUEST_UPLOAD_FILE:
            raise ValueError('Request Field must be REQUEST_UPLOAD_FILE')
        super().__init__(header)
        self.file_path = file_path

    def get_message_stream(self) -> io.BufferedReader:
        return super().get_message_stream()