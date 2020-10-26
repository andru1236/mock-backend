from typing import List
from modules.api_instance.domain.api import Param
from modules.api_instance.domain.api import Response
from modules.shared.domain.errors import DomainBadRequestError


class Resource:
    def __init__(self, method: str, response: Response, params: List[Param]=[]) -> None:
        self.method = method
        self.response = response.value
        self.params = params

    def is_equals(self, resource):
        return self.method == resource.method

    def add_params(self, param: Param):
        if self._find_param_index(param):
            raise DomainBadRequestError(f'This param "{param.param}" already exist')
        self.params.append(param)

    def replace_params(self, param: Param):
        param_index =  self._find_param_index(param)
        if param_index is None:
            raise DomainBadRequestError(f'Param "{param.param}" not found')
        self.params[param_index] = param

    def remove_params(self, param: Param):
        param_index =  self._find_param_index(param)
        if param_index is None:
            raise DomainBadRequestError(f'This params {param.param} not exist')
        del self.params[param_index]

    def get_object_dict(self):
        return {
            'method': self.method,
            'response': self.response,
            'params': [param.__dict__ for param in self.params]
        }

    def _find_param_index(self, new_param: Param):
        for index, param in enumerate(self.params):
            if param.param == new_param.param:
                return index
