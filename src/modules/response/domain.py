from typing import List
from dataclasses import dataclass, field
from datetime import datetime

from modules.api_instance.domain.api import Response as ResponseAPIInstance
from modules.shared.domain.errors import DomainBaseError


@dataclass
class RoutesTracking:
    path: str
    method: str
    query_params: List[str] = field(default_factory=list)
    date: datetime = field(default=datetime.now())

@dataclass
class TrackingAssignation:
    api_id: str
    routes: List[RoutesTracking] = field(default_factory=list)


@dataclass
class Response:
    name: str
    response: ResponseAPIInstance
    tracking_assignation: List[TrackingAssignation] = field(default_factory=list)
    _id: str = None
    created_on: datetime = field(default=datetime.now())

    def __post_init__(self):
        self.response = ResponseAPIInstance(self.response)


def validation(response: Response):
    if not isinstance(response.name, str):
        raise DomainBaseError('The name should be string or different to None')

    if not isinstance(response.response, ResponseAPIInstance):
        raise DomainBaseError('The response should be a dict or list of dicts')

    if response.tracking_assignation is not None and not isinstance(response.tracking_assignation, list):
        raise DomainBaseError('The assignation should be list of objects')

    return response


def track_response(response, api):
    pass
