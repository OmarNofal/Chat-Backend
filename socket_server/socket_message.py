
import json
import struct

class socket_message:

    def __init__(self,
    header: dict = {},
    content: bytes = b''
    ) -> None:
        self.h = header
        self.c = content


    def get_message_bytes(self) -> bytes:
        header = json.dumps(self.h).encode('utf-8')
    
        header_len = len(header)
        proto_header = struct.pack(">H", header_len)

        b = proto_header + header + self.c
        return b

    def __getitem__(self, key):
        return self.h[key]
    
    def __setitem__(self, key, value):
        self.h[key] = value

    def __delitem__(self, key):
        del self.h[key]

    @property
    def header(self) -> dict:
        return self.h  

    @property
    def content(self) -> bytes:
        return self.c