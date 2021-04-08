from dataclasses import dataclass

from modules.shared.domain import IUseCase, errors
from modules.shared.infrastructure import process_manager, logger
from ..infrastructure import file_manager, command_lines
from ..domain import Device


@dataclass
class StartSimulationCommand:
    dev_id: str


class StartSimulation(IUseCase):
    def __init__(self, respository) -> None:
        self.repository = respository

    def execute(self, command: StartSimulationCommand) -> None:
        logger.info(f"Start to simulate the Device: {command.dev_id}")
        dev: Device = self.repository.search(command.dev_id)

        if dev.is_running:
            raise errors.DomainBadRequestError(f"The device: {dev.id} is running")

        file_manager.mount_agent_db_for_device(dev.id, dev.agent_db)

        mgr = process_manager.ProcessManager()
        mgr.run_cli_as_process(
            dev.id,
            command_lines.run_snmpsimd_agent,
            (command_lines.get_path_db(dev.id), dev.port),
            dev.port,
            []
        )

        dev.is_running = True
        self.repository.save(dev)
