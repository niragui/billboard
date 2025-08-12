
class ConnectionError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DateError(KeyError):
    def __init__(self, *args):
        super().__init__(*args)