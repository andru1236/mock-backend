import psutil
from dataclasses import dataclass
from typing import Any, List, Dict, Callable

from ..domain.errors import DomainBaseError

from .utils import SingletonDecorator
from .logger import logger


class NotEnoughResources(DomainBaseError):
    pass


class PortIsBusy(DomainBaseError):
    pass


def valid_cpu_resources(total_process: int) -> bool:
    REQUIRED_MEM = 100 * 1024 * 1024
    INSTANCES_PER_CORE = 2

    def is_there_enough_cores():
        try:
            cpus = psutil.Process().cpu_affinity()
        except:
            cpus = psutil.cpu_count()
        return len(total_process) < len(cpus) * INSTANCES_PER_CORE

    def is_there_momery():
        mem = psutil.virtual_memory()
        return mem.available > REQUIRED_MEM

    if not is_there_enough_cores():
        raise NotEnoughResources(f'Not enough CPU Cores to start the process')

    if not is_there_momery():
        raise NotEnoughResources(f'Not enough Memory to start the process')

    return True


def valid_is_port_avaiable(used_ports: List[int], port_to_use) -> bool:

    for used_port in used_ports:
        if used_port == port_to_use:
            raise PortIsBusy(f'Exists other process run on port: {port_to_use}')
    return True
    
@dataclass
class Process:
    id: str
    port: int
    validators: List[Any]
    multiprocessing_obj: Any
    start_func: Callable
    stop_func: Callable


@SingletonDecorator
class ProcessManager:

    def __init__(self) -> None:
        self.processes: Dict[str, Process] = {}

    def run_process(self, process: Process):
        
        #valid_cpu_resources(len(self.processes))
        valid_is_port_avaiable(
            list(map(lambda process: process.port, self.processes.values())),
            process.port
        )

        for valid_process in process.validators:
            valid_process()

        self.processes[process.id] = process

        try:
            logger.info(f"kick off a process pid: {process.id}")
            process.start_func()
        except Exception as error:
            logger.error(f'the process was not able to kick off')
            raise error

    def stop_process(self, id):
        process = self.processes.get(id)
        logger.info(f'The process process: {process} will be stop')
        if process:
            process.stop_func()
            logger.info(f'The process was stoped successfull')
            logger.info(f'Start to removing the process from the store')
            del self.processes[id]
