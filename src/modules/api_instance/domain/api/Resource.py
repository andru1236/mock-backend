from typing import List
from modules.api_instance.domain.api import Param
from modules.api_instance.domain.api import Response


class Resource:
    def __init__(self, method: str, response: Response, params: List[Param]=[]) -> None:
        self.method = method
        self.response = response.value
        self.params = params

    def is_equals(self, resource):
        return self.method == resource.method

    def add_params(self, param:Param):
        if self._contains_param(param):
            raise Exception('Params already registered')
        self.params.append(param)
    
    def get_object_dict(self):
        return {
            'method': self.method,
            'response': self.response,
            'params': [param.__dict__ for param in self.params]
        }

    def _contains_param(self, new_param: Param):
        for param in self.params:
            if param.param == new_param.param:
                return param
