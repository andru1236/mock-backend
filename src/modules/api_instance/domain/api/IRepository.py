from modules.api_instance.domain.api import ApiInstance


class IRepository:

    def save(self, api_instance: ApiInstance) -> None: pass

    def search(self, api_id: str) -> ApiInstance: pass

    def delete(self, api_id: str) -> None: pass
