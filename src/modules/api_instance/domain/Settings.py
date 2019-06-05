from datetime import datetime


class Settings:

    def __init__(self, enabled: bool = False, created_on: str = str(datetime.now())) -> None:
        self.enabled = enabled
        self.created_on = created_on
