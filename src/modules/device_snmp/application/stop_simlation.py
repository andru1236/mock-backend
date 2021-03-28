from dataclasses import dataclass
from modules.shared.domain.IUseCase import IUseCase
from modules.shared.infrastructure import process_manager, logger
from ..infrastructure import file_manager


@dataclass
class StopSimulationCommand:
    dev_id: str


class StopSimulation(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: StopSimulationCommand) -> None:
        logger.info(f"Stop simulation for device: {command.dev_id}")
        mgr = process_manager.ProcessManager()
        mgr.stop_process(command.dev_id)
        file_manager.remove_agent_db_folder(command.dev_id)
