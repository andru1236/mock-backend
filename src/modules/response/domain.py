from typing import List
from dataclasses import dataclass
from datetime import datetime

from modules.api_instance.domain.api import Response as ResponseAPIInstance
from modules.shared.domain.errors import DomainBaseError


@dataclass
class RoutesTracking:
    path: str
    method: str
    query_params: List[str]
    date: datetime

@dataclass
class TrackingAssignation:
    api_id: str
    routes: List[RoutesTracking]


@dataclass
class Response:
    name: str
    response: ResponseAPIInstance
    tracking_assignation: List[TrackingAssignation]
    _id: str = None


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
