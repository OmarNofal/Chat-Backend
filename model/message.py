from model.model import model
from datetime import datetime

class message(model):
    
    def __init__(self, 
    id: str = None, 
    from_id: str = None,
    to_id: str = None,
    time: datetime = datetime.now(),
    media_id: str = None,
    message_text: str = ''
    ):
        super().__init__(id)
        self.message_text = message_text
        self.from_id = from_id
        self.to_id = to_id
        self.media_id = media_id
        self.time = time

    def as_dict(self) -> dict:
        res = super().as_dict()
        res['from_id'] = self.from_id
        res['to_id'] = self.to_id
        res['media_id'] = self.media_id
        res['message_text'] = self.message_text
        res['time'] = self.time
        return res
