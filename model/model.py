

class model:

    def __init__(self, id: str):
        self.id = id

    def as_dict(self) -> dict:
        return {'id': self.id}