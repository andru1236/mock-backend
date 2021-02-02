from modules.shared.domain.errors import DomainBadRequestError


class Response:
    def __init__(self, response) -> None:
        # if not isinstance(response, dict):
        #     raise DomainBadRequestError('The response is not a json')
        # elif not isinstance(response, list):
        #     raise DomainBadRequestError('The response is not a json')

        if isinstance(response, dict) or isinstance(response, list):
            self.value = response
        else:
            raise DomainBadRequestError('The response is not a json')
        # try:
        #     loads(response)
        #     self.value = response
        # except ValueError:
        #     raise DomainBadRequestError('The response is not a json')

    def __repr__(self) -> str:
        return f'Response API Domain {str(self.value)}'
