from model.message import message


class media_message(message):


    def __init__(
        self,
        id: str = None,
        from_id: str = None,
        to_id: str = None,
        time: datetime = datetime.now(),
        media_id: str = None,
        message_text: str = ''
    ):
        super().__init__(
            id=id,
            from_id=from_id,
            to_id=to_id,
            time=time,
            message_text=message_text
        )