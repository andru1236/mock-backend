import os
import psutil
from modules.api_instance.domain.builder_server.validator import Validator
from modules.api_instance.domain.builder_server.errors import PortIsBusy


class AvailabilityValidator(Validator):
    def validate(self, instances, api):
        if self._port_is_busy(instances, api.port.value):
            raise PortIsBusy(
                f'Exists other server run on port: {api.port.value}')

    def _port_is_busy(self, instances, port: int):
        if port == int(os.environ.get('PORT')):
            return True
        for instance_flask in instances:
            if instance_flask.port == port:
                return True
        return False
