from dataclasses import dataclass

from modules.api_instance.domain.api import Response as ResponseAPIInstance

# TODO research best way to handle the little entities
@dataclass
class Response:
    _id: str
    response: ResponseAPIInstance
    assignation_meta: list
