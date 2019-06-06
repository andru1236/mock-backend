from modules.api_instance.application.register_api import RegisterApi
from modules.api_instance.application.register_api import RegisterApiCommand

from modules.api_instance.infrastructure import FakeRepository


def test_register_api_success():
    repository = FakeRepository()
    use_case = RegisterApi(repository)

    not_exist_data = 0
    assert len(repository.apis) == not_exist_data

    common_port = 8000
    command = RegisterApiCommand(common_port)
    use_case.execute(command)

    one_element_in_repository = 1

    assert len(repository.apis) == one_element_in_repository
