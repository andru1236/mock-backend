import pytest

from test.modules.api_instance.domain.Response_test import get_response
from test.modules.api_instance.domain.Port_test import get_port
from test.modules.api_instance.domain.Route_test import get_users_routes_crud
from modules.api_instance.infrastructure import FakeRepository


@pytest.fixture(scope='function')
def repository():
    return FakeRepository()