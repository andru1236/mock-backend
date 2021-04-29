from backend.api_instance.application.register_api import RegisterApi
from backend.api_instance.application.register_api import RegisterApiCommand

from backend.api_instance.infrastructure import FakeRepository


def test_register_api_success():
    repository = FakeRepository()
    use_case = RegisterApi(repository)

    not_exist_data = 0
    assert len(repository.apis) == not_exist_data

    common_port = 8000
    name = 'test'
    command = RegisterApiCommand(name, common_port)
    use_case.execute(command)

    one_element_in_repository = 1

    assert len(repository.apis) == one_element_in_repository


def test_register_many_apis_success():
    repository = FakeRepository()
    use_case = RegisterApi(repository)

    not_exist_data = 0
    assert len(repository.apis) == not_exist_data

    name = 'test'
    common_port = [8000, 5000, 8080, 3000, 3001, 3002, 3003, 4000]

    commands_will_be_execute = []
    for port in common_port:
        commands_will_be_execute.append(RegisterApiCommand(name, port))

    inserted_apis = 0
    for command in commands_will_be_execute:
        use_case.execute(command)
        inserted_apis += 1
        assert len(repository.apis) == inserted_apis


def test_register_many_apis_with_same_port():
    repository = FakeRepository()
    use_case = RegisterApi(repository)

    not_exist_data = 0
    assert len(repository.apis) == not_exist_data

    name = 'test'
    same_ports = [8000, 8000, 8000, 8000, 8000]

    commands_will_be_execute = []
    for port in same_ports:
        commands_will_be_execute.append(RegisterApiCommand(name, port))

    inserted_apis = 0
    for command in commands_will_be_execute:
        use_case.execute(command)
        inserted_apis += 1
        assert len(repository.apis) == inserted_apis
