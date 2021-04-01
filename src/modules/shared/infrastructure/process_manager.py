import psutil
import multiprocessing
from dataclasses import dataclass
from typing import Any, List, Dict, Callable, Tuple

from ..domain.errors import DomainBaseError

from .utils import SingletonDecorator
from .logger import logger


# TODO Move all exceptions to new module exceptions in root infrastructure
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
            return total_process < len(cpus) * INSTANCES_PER_CORE
        except:
            cpus = psutil.cpu_count()
            return total_process < cpus * INSTANCES_PER_CORE

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
    proc_obj: Any
    start_func: Callable
    stop_func: Callable


@SingletonDecorator
class ProcessManager:

    def __init__(self) -> None:
        self.processes: Dict[str, Process] = {}

    def run_obj_as_process(
            self, id: str, obj: Any, exec_func: Callable, params: Tuple[Any], port: int,
            validators: List[Callable] = None
    ):
        logger.info(f"Packing obj: {obj} to run as a process")

        multi_proc_obj = multiprocessing.Process(target=exec_func, args=params)

        def start():
            multi_proc_obj.start()

        def stop():
            multi_proc_obj.terminate()

        process = Process(
            id,
            port,
            validators if validators is not None else [],
            multi_proc_obj,
            start,
            stop
        )
        self.run_process(process)

    def run_cli_as_process(self, id, func, params, port, validators=None):
        logger.info(f"Packing func: {func} to run as a process")

        try:
            cli_process = func(*params)
        except Exception as error:
            logger.critical(f"The process was not able to run: {error}")
            # TODO raise custom error
            raise error

        def stop():
            cli_process.terminate()
            cli_process.kill()

        process = Process(
            id,
            port,
            validators if validators is not None else [],
            cli_process,
            lambda: logger.info(
                f"process already was kicked off -> PID: {cli_process.pid}"
            ),
            stop,
        )

        self.run_process(process)

    def run_process(self, process: Process):
        self.run_validators(process)
        self.processes[process.id] = process

        try:
            logger.info(f"kick off a process ID: {process.id}")
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

    def run_validators(self, process):
        try:
            valid_cpu_resources(len(self.processes))
            valid_is_port_avaiable(
                list(map(lambda process: process.port, self.processes.values())),
                process.port
            )
            for valid_process in process.validators:
                valid_process()

        except Exception as error:
            if process.id in self.processes:
                try:
                    self.processes[process.id].stop_func()
                    del self.processes[process.id]
                except Exception as error:
                    del self.processes[process.id]

            # TODO raise customer Error
            raise error
