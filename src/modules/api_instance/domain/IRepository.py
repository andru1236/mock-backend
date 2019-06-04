from modules.api_instance.domain import ApiInstance


class IRepository:

    def save(self, api_instance: ApiInstance) -> None: pass

    def search(self, api_id: str) -> ApiInstance: pass
