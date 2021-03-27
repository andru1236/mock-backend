import psutil
from dataclasses import dataclass
from typing import Any, List, Dict

from ..domain.errors import DomainBaseError

from .utils import SingletonDecorator
from .logger import logger


class NotEnoughResources(DomainBaseError):
    pass


class PortIsBusy(DomainBaseError):
    pass


class ServerIsRunning(DomainBaseError):
    pass


class ServerNeverWasStarting(DomainBaseError):
    pass


def valid_cpu_resources(total_process):
    REQUIRED_MEM = 100 * 1024 * 1024
    INSTANCES_PER_CORE = 2

    def is_there_enough_cores():
        cpus = psutil.Process().cpu_affinity()
        return len(total_process) < len(cpus) * INSTANCES_PER_CORE

    def is_there_momery():
        mem = psutil.virtual_memory()
        return mem.available > REQUIRED_MEM

    if not is_there_enough_cores():
        raise NotEnoughResources(f'Not enough CPU Cores to start the process')

    if not is_there_momery():
        raise NotEnoughResources(f'Not enough Memory to start the process')

    return True


@dataclass
class Process:
    id: str
    pid: int
    multiprocessing_obj: Any
    validators: List[Any]
    port: int


@SingletonDecorator
class ProcessManager:

    def __init__(self) -> None:
        self.processes: Dict[str, Process] = {}

    def run_process(self, process: Process):
        if (valid_cpu_resources(len(self.processes))):
            for valid_process in process.validators:
                valid_process()

        self.processes[process.id] = process

        try:
            logger.info(f"kick off a process pid: {process.pid}")
            process.multiprocessing_obj.start()
        except Exception as error:
            logger.error(f'the process was not able to kick off')
            raise error

    def stop_process(self, id):
        process = self.processes.get(id)
        logger.info(f'The process process: {process} will be stop')
        if process:
            process.multiprocessing_obj.terminate()
            process.multiprocessing_obj.join()
            logger.info(f'The process was stoped successfull')
            logger.info(f'Start to removing the process from the store')
            del process[id]

