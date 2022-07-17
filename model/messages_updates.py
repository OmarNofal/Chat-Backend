from .model import model



class messages_updates(model):
    """
    Represents the message updates that will be sent to the user
    when he asks for new messages
    """

    def __init__(
        self, 
        id: str,
        user_id: str,
        received_messages,
        read_messages
        ):
        super().__init__(id)
        self.user_id = user_id
        self.received_messages: list[str] = received_messages
        self.read_messages: list[str] = read_messages

    def add_received_message(self, message_id: str):
        self.received_messages += [message_id]
    
    def add_read_message(self, message_id: str):
        self.read_messages += [message_id]
    
    def remove_received_message(self, message_id: str):
        try:
            self.received_messages.remove(message_id)
        except:
            pass
    
    def remove_read_message(self, message_id: str):
        try: 
            self.read_messages.remove(message_id)
        except:
            pass

    def as_dict(self) -> dict:
        result = super().as_dict()
        result['user_id'] = self.user_id
        result['received_messages'] = self.received_messages
        result['read_messages'] = self.read_messages
        return result
