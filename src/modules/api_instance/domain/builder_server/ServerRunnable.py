class ServerRunnable:

    def __init__(self, _id: str, process, port: int) -> None:
        self._id = _id
        self.process = process
        self.port = port

    def stop_server(self):
        self.process.terminate()
        self.process.join()
