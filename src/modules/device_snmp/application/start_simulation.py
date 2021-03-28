from dataclasses import dataclass

from modules.shared.domain import IUseCase
from modules.shared.infrastructure import process_manager, logger
from ..infrastructure import file_manager, command_lines


@dataclass
class StartSimulationCommand:
    dev_id: str


class StartSimulation(IUseCase):
    def __init__(self, respository) -> None:
        self.repository = respository

    def execute(self, command: StartSimulationCommand) -> None:
        logger.info(f"Start to simulate the Device: {command.dev_id}")
        dev = self.repository.search(command.dev_id)
        file_manager.mount_agent_db_for_device(dev._id, dev.agent_db)

        cli_process = command_lines.run_snmpsimd_agent(
            command_lines.get_path_db(dev._id), dev.port
        )

        def kill_process():
            cli_process.terminate()
            cli_process.kill()

        process = process_manager.Process(
            dev._id,
            dev.port,
            [],
            cli_process,
            lambda: logger.info(f"process already was kicked off -> PID: {cli_process.pid}"),
            kill_process,
        )

        mgr = process_manager.ProcessManager()
        mgr.run_process(process)
