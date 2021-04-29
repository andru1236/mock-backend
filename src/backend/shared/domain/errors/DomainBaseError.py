class DomainBaseError(Exception):

    def __init__(self, message: str, payload=None) -> None:
        self.errorName = self.__class__.__name__
        self.message = message
        self.payload = payload

    def __str__(self):
        if self.payload:
            return f'{self.message} - Payload:{self.payload}'
        return self.message
