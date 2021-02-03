import pytest
import dataclasses
import datetime

from typing import Any
from modules.response import domain

from modules.shared.domain.errors import DomainBadRequestError


def test_respose():
    name = 'test_response'
    response = {'test': 'test'}
    result = domain.Response(name, response)
    assert result.name == name
    assert result.response == response


@pytest.fixture(
    params=[
        "base",
        "with_tracking",
        "with_trancking_and_routes"
    ],
    scope='function'
)
def dict_test_case(request):
    current_date = datetime.datetime.now()

    @dataclasses.dataclass
    class test_case:
        dict_to_build: dict
        built_dict: dict
        type_class_tracking: Any
        type_class_tracking_route: Any
    
    base = test_case(
        {
            'name': 'test_response',
            'response': {'test': 'test'},
            'created_on': current_date
        },
        {
            'name': 'test_response',
            'response': {'test': 'test'},
            'tracking_assignations': [],
            '_id': None,
            'created_on': current_date
        },
        None,
        None
    )

    with_tracking = test_case(
        {
            'name': 'test_response',
            'response': {'test': 'test'},
            'tracking_assignations': [{'api_id': '12345', 'routes': []}],
            'created_on': current_date
        },
        {
            'name': 'test_response',
            'response': {'test': 'test'},
            'tracking_assignations': [{'api_id': '12345', 'routes': []}],
            '_id': None,
            'created_on': current_date
        },
        domain.TrackingAssignation,
        list
    )

    with_tracking_and_routes = test_case(
        {
            'name': 'test_response',
            'response': {'test': 'test'},
            'tracking_assignations': [{'api_id': '12345', 'routes': [
                {
                    'path': '/test_end_point',
                    'method': 'POST',
                    'query_params': [],
                    'date': current_date
                }
            ]}],
            '_id': None,
            'created_on': current_date
        },
        {
            'name': 'test_response',
            'response': {'test': 'test'},
            'tracking_assignations': [{'api_id': '12345', 'routes': [
                {
                    'path': '/test_end_point',
                    'method': 'POST',
                    'query_params': [],
                    'date': current_date
                }
            ]}],
            '_id': None,
            'created_on': current_date
        },
        domain.TrackingAssignation,
        domain.RoutesTracking
    )

    fixture_map ={
        'base': base,
        'with_tracking': with_tracking,
        'with_tracking_and_routes': with_tracking_and_routes
    }

    return fixture_map[request.param]


@pytest.mark.parametrize(
    "dict_test_case",
    ["base", "with_tracking",  "with_tracking_and_routes"],
    indirect=["dict_test_case"]
)
def test_create_respose_from_dict_default(dict_test_case):
    result = domain.Response(**dict_test_case.dict_to_build)
    assert dataclasses.asdict(result) == dict_test_case.built_dict

    if len(result.tracking_assignations):
        assert isinstance(result.tracking_assignations[0], dict_test_case.type_class_tracking)
        if len(result.tracking_assignations[0].routes):
            assert isinstance(result.tracking_assignations[0].routes[0], dict_test_case.type_class_tracking_route)


def test_valid_response_successful():
    result = domain.Response('test_response', {'test': 'test'})
    result2 = domain.Response('test_response', [{'test': 'test'}])
    assert domain.validation(result)
    assert domain.validation(result2)


@pytest.mark.parametrize(
    "response",
    [
        domain.Response(1, {'test': 'test'}),
        domain.Response("something", 123),
        domain.Response("something", '123'),
        domain.Response(True, False)
    ]
)
def test_valid_response__unseucessful(response):
    with pytest.raises(DomainBadRequestError):
        domain.validation(response)