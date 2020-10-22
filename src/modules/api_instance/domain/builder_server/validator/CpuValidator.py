import psutil
from modules.api_instance.domain.builder_server.validator import Validator
from modules.api_instance.domain.builder_server.errors import NotEnoughResources


class CpuValidator(Validator):
    REQUIRED_MEM = 100 * 1024 * 1024
    INSTANCES_PER_CORE = 2

    def validate(self, instances, api):

        if not self._are_enough_cores(instances):
            raise NotEnoughResources(
                f'Not enough CPU Cores to start the API: {api._id}')

        if not self._is_enough_memory():
            raise NotEnoughResources(
                f'Not enough Memory to start the API: {api._id}')

    def _are_enough_cores(self, instances):
        cpus = psutil.Process().cpu_affinity()
        return len(instances) < len(cpus) * self.INSTANCES_PER_CORE

    def _is_enough_memory(self):
        mem = psutil.virtual_memory()
        return mem.available > self.REQUIRED_MEM
