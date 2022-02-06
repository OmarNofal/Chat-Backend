from model.model import model
from datetime import datetime

class message(model):
    
    def __init__(self, 
    id: str = None, 
    from_id: str = None,
    to_id: str = None,
    time: datetime = datetime.now(),
    message_text: str = ''
    ):
        super().__init__(id)
        self.message_text = message_text
        self.from_id = from_id
        self.to_id = to_id
        self.type = 'text_message'


