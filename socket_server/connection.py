import selectors
import socket

from .messages.socket_message import socket_message
from .socket_reader import socket_reader
from .socket_writer import socket_writer


class connection:

    def __init__(self, selector: selectors.DefaultSelector, sock: socket.socket) -> None:
        self.sock = sock
        self.reader = socket_reader(sock)
        self.writer = socket_writer(sock)
        self.selector = selector
        self.is_closed = False
        self.user_id = None
        self.sent_messages: list[socket_message] = []

    def process_events(self, mask):
        if (self.is_closed):
            return

        # check message we are sending
        current_msg: socket_message = self.writer.messages[0] if (len(self.writer.messages) > 0) else None

        # write queued message
        if mask & selectors.EVENT_WRITE:
            self._write_event()
        
        #TODO we removed a line here 
        # read messages
        if mask & selectors.EVENT_READ:
            self._read_event()

    def _read_event(self):
        self.reader.process_events()
        if self.reader.is_closed:
            self.close()
        
    def _write_event(self):
        if not self.writer.has_messages():
            self.selector.modify(self.sock, selectors.EVENT_READ, data=self)
        else:
            self.writer.process_events()

    def send_message(self, message: socket_message):
        self.writer.enqueue_message(message)
        new_mask = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.modify(self.sock, new_mask, data=self)

    def has_messages(self):
        return self.reader.has_messages()

    def get_messages(self):
        msgs = []
        while self.reader.has_messages():
            msgs.append(self.reader.pop_message())
        return msgs

    def close(self):
        self.selector.unregister(self.sock)
        self.sock.close()
        self.is_closed = True