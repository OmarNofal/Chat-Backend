import socket
import io

from zmq import Socket
from socket_server.messages.socket_message import *

class socket_writer:

    def __init__(self, sock: socket.socket) -> None:
        self.messages: list[socket_message] = []
        self.sock = sock
        self.stream: io.BufferedReader = None
        self.buffer = b''
        self.is_closed = False


    # TODO 
    # two objects needed (stream object) and (bytes buffer object)
    # read from stream into buffer and try to send all of them
    # when buffer is empty just refill it untill the stream is empty

    def process_events(self):
        
        if len(self.messages) == 0:
            return
        if not self.stream:
            self.stream = self.messages[0].get_message_stream()
    
        if not self.buffer:
            self.buffer = self.stream.read(4096)
            if self.buffer == b'':
                # nothing was read from the stream so we delete the message
                self.stream.close()
                self.messages.pop(0)
                self.stream = None
                return

        self._write_buffer()


    def _write_buffer(self):
        try:
            sent = self.sock.send(self.buffer)
            self.buffer = self.buffer[sent:]
        except socket.error as e:
            self.is_closed = True
            print("Error occured while writing message " + str(e))

    def enqueue_message(self, msg: socket_message):
        self.messages.append(msg)

    def has_messages(self) -> bool :
        return len(self.messages) > 0

