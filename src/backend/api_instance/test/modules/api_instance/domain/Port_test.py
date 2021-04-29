import pytest
from backend.api_instance.domain import Port
from backend.shared.domain.errors import DomainBadRequestError


@pytest.fixture
def get_port(number_port=8000):
    return Port(number_port)


def test_create_port_success():
    test_port = 8000
    port = Port(test_port)
    assert port.value == test_port


def test_create_port_on_reserved_number_fail():
    with pytest.raises(DomainBadRequestError):
        for invalid_port in range(80):
            Port(invalid_port)


def test_create_port_that_not_exist_fail():
    with pytest.raises(DomainBadRequestError):
        for port_that_no_exist in range(65535, 70000):
            Port(port_that_no_exist)


def test_create_port_with_bad_arguments_fail():
    with pytest.raises(DomainBadRequestError):
        Port('5000')
