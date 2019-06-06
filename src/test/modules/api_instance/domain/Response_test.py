import pytest

from modules.api_instance.domain import Response
from modules.shared.domain.errors import DomainBadRequestError


@pytest.fixture
def get_response():
    response_string_json = '{"name": "Andres Gutiererz", "range": "dev"}'
    return Response(response_string_json)


def test_create_response_success():
    response_string_json = '{"name": "Andres Gutiererz", "range": "dev"}'
    response = Response(response_string_json)
    assert response.value == response_string_json


def test_create_response_string_json_with_single_quote():
    with pytest.raises(DomainBadRequestError):
        response_string_json = "{'name': 'Andres Gutiererz', 'range': 'dev'}"
        Response(response_string_json)


def test_create_response_with_bad_format_json():
    with pytest.raises(DomainBadRequestError):
        response_string_json = "{test}"
        Response(response_string_json)


def test_create_response_with_response_blank():
    response_value = '{}'
    response = Response(response_value)
    assert response.value == response_value
