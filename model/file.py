from datetime import datetime
from model.model import model


class file(model):

    def __init__(
        self, 
        id: str = None,
        user_id: str = '',
        file_name: str = '',
        file_extension: str = 'txt',
        upload_date: datetime = datetime.now()
    ):
        super().__init__(id)
        self.user_id = user_id
        self.file_name = file_name
        self.file_extension = file_extension
        self.upload_date = upload_date

    def as_dict(self) -> dict:
        res = {
            'id': self.id,
            'file_name': self.file_name,
            'file_extension': self.file_extension,
            'upload_date': str(self.upload_date)
        }
        return res