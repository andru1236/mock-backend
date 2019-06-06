from modules.api_instance import RegisterApi
from modules.api_instance import RegisterApiCommand
from modules.api_instance import UpdateApi
from modules.api_instance import UpdateApiCommand
from modules.api_instance.infrastructure import FakeRepository


def test_update_api():
    repository = FakeRepository()
    register_api = RegisterApi(repository)
    use_case = UpdateApi(repository)

    port_test_base = 8000
    register_api.execute(RegisterApiCommand(port_test_base))

    api_id = repository.apis[0]._id
    api = repository.search(api_id)

    assert api.port.value == port_test_base

    new_port = 5000
    use_case.execute(UpdateApiCommand(api_id, new_port))
    assert api.port.value == new_port
