from model import model
from datetime import datetime

class request(model):

    def __init__(self, 
    id: str = None,
    sender_id: str = None,
    receiver_id: str = None,
    time: datetime = datetime.now()
    ):
        super().__init__(id)
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.time = time
    
    def as_dict() -> dict:
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id
        }