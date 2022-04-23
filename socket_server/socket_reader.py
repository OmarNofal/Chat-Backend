import json
import selectors
import socket
import struct

from .socket_message import socket_message as message


class socket_reader:
    """ Reads data from socket and encodes the 
    data in Message objects """
    def __init__(self, sock: socket.socket):
        self.sock: socket.socket = sock
        self.buffer = b''
        self.header_len = None
        self.header_read = False
        self.messages = []
        self.is_closed = False

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

            if "content-length" not in header_json:
                print('Header formatted incorrectly (content-length not found)')
                self.close()
                return

            self.content_length = header_json["content-length"]
            self.buffer = self.buffer[header_len:]

            self.header = header_json
            self.header_read = True
    
    def _read_content(self):
        if len(self.buffer) >= self.content_length:
            content = self.buffer[:self.content_length]
            msg = message(header = self.header, content = content)
            self.messages.append(msg)

            self.header_len = None
            self.header_read = False
            self.header = None
            self.content_length = None
    

    def pop_message(self) -> message:
        msg = self.messages.pop()
        return msg

    def has_messages(self):
        return len(self.messages) > 0
