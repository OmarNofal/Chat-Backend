import socket


class socket_writer:

    def __init__(self, sock: socket.socket) -> None:
        self.messages = []
        self.sock = sock
        self.buffer = None


    def process_events(self):
        if len(self.messages) == 0:
            return
        if not self.buffer:
            self.buffer = self.messages[0].get_message_bytes()
        self._write_buffer()
        if self.buffer == b'':
            self.messages.pop(0)



    def _write_buffer(self):
        try:
            sent = self.sock.send(self.buffer)
            self.buffer = self.buffer[:sent]
        except Exception as e:
            print("Error occured while writing message " + str(e))

    def enqueue_message(self, msg):
        self.messages.append(msg)

    def has_messages(self):
        return len(self.messages) > 0

