from .model import model


class friends(model):
    """ Represents friend relationship between 2 people 
        u1_id < u2_id
    """
    def __init__(self, 
    id: str = None,
    u1_id: str = '',
    u2_id: str = ''
    ):
        super().__init__(id)
        self.u1_id = u1_id
        self.u2_id = u2_id
    
    def as_dict(self):
        return {
            'id': self.id,
            'u1_id': self.u1_id,
            'u2_id': self.u2_id
        }