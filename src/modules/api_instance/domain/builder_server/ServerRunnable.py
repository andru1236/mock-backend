class ServerRunnable:

    def __init__(self, _id: str, process) -> None:
        self._id = _id
        self.process = process

    def stop_server(self):
        self.process.terminate()
        self.process.join()
