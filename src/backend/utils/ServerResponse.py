class ServerResponse:

    def __init__(self, data, status) -> None:
        self.meta = {'statusCode': status}
        if data is None:
            self.data = {}
        else:
            self.data = {**data}
