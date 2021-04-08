from dataclasses import dataclass

from modules.shared.domain import IUseCase, errors
from modules.shared.infrastructure import process_manager, logger

from ..domain import Device
from ..infrastructure import file_manager


@dataclass
class StopSimulationCommand:
    dev_id: str


class StopSimulation(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: StopSimulationCommand) -> None:
        logger.info(f"Stop simulation for device: {command.dev_id}")
        dev: Device = self.repository.search(command.dev_id)

        if not dev.is_running:
            raise errors.DomainBadRequestError(
                f"The device: {dev.id} never started to running"
            )
        mgr = process_manager.ProcessManager()
        mgr.stop_process(command.dev_id)
        file_manager.remove_agent_db_folder(command.dev_id)

        dev.is_running = False
        self.repository.save(dev)
