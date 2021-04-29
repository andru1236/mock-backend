from backend.api_instance import DeleteApi
from backend.api_instance import DeleteApiCommand
from backend.api_instance import RegisterApi
from backend.api_instance import RegisterApiCommand
from backend.api_instance.infrastructure import FakeRepository


def test_delete_api():
    repository = FakeRepository()
    register_api = RegisterApi(repository)
    register_api.execute(RegisterApiCommand('test', 8000))

    inserted_one_api_instance = 1
    assert len(repository.apis) == inserted_one_api_instance

    api_id = repository.apis[0]._id

    use_case = DeleteApi(repository)
    use_case.execute(DeleteApiCommand(api_id))

    without_api = 0

    assert len(repository.apis) == without_api
