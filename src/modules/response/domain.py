from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from modules.shared.domain.errors import DomainBadRequestError


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

    def __post_init__(self):
        if len(self.routes):
            self.routes = list(
                map(lambda route: RoutesTracking(**route) if not isinstance(route, RoutesTracking) else route , self.routes))


######################
######### MAIN CLASS 
######################
@dataclass
class Response:
    name: str
    response: dict or list
    tracking_assignations: List[TrackingAssignation] = field(default_factory=list)
    _id: str = None
    created_on: datetime = field(default=datetime.now())

    def __post_init__(self):
        if len(self.tracking_assignations):
            self.tracking_assignations = list(
                map(lambda track: TrackingAssignation(**track) if not isinstance(track, TrackingAssignation) else track , self.tracking_assignations))


def validation(response: Response):
    if not isinstance(response.name, str):
        raise DomainBadRequestError('The name should be string or different to None')

    if not isinstance(response.response, dict):
        if not isinstance(response.response, list):
            raise DomainBadRequestError('The response should be a dict or list of dicts')


    if response.tracking_assignations is not None and not isinstance(response.tracking_assignations, list):
        raise DomainBadRequestError('The assignation should be list of objects')

    return response


# TODO: refactor the tracking meta data
def track_response(response: Response, meta):
    try:
        if meta.api_id and meta.path and meta.method:
            filtered_assignation: List[TrackingAssignation] = list(filter(lambda x : x.api_id == meta.api_id, response.tracking_assignations))

            if len(filtered_assignation) != 0:
                filtered_routes: List[RoutesTracking] = list(
                    filter(
                        lambda y: y.path == meta.path and y.method == meta.method,
                        filtered_assignation[0].routes
                    )
                )
                if len(filtered_routes) == 0:
                    filtered_assignation[0].routes.append(RoutesTracking(meta.path, meta.method))

                return response

            track_assignation = TrackingAssignation(meta.api_id)
            track_route = RoutesTracking(meta.path, meta.method)

            track_assignation.routes.append(track_route)
            response.tracking_assignations.append(track_assignation)

            return response

    except Exception:
        raise DomainBadRequestError('The Api meta information are not valid')
    
