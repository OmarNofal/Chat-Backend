
from abc import ABC

class api_response(ABC):

    def __init__(self, result: str) -> None:
        self.content = {}
        self.content['result'] = result
        super().__init__()

    def __getitem__(self, key):
        return self.content[key]

    def __setitem__(self, key, value):
        self.content[key] = value
    

class error_reponse(api_response):

    def __init__(self, msg: str) -> None:
        super().__init__('error')
        self.content['message'] = msg

class success_response(api_response):

    def __init__(self) -> None:
        super().__init__('success')