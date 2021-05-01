from dataclasses import dataclass

from backend.shared.domain import IUseCase, errors
from backend.shared.infrastructure import process_manager, logger
from ..infrastructure import file_manager, command_lines, snmp_object_parser
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

        if dev.agent_db is None:
            raise errors.DomainBadRequestError(f"The device: {dev.id} does not have DB to simulate")

        parser = snmp_object_parser.SnmpObjectParser()

        logger.info("Parsing to the rec file to mount the device")
        agent_db_to_mount = dev.agent_db
        type_of_agent_db = parser.get_type_of_agent_db(agent_db_to_mount)

        if type_of_agent_db == snmp_object_parser.SNMPWALK:
            logger.info("The agent db is snmpwalk file")
            file_rows = agent_db_to_mount.split("\n")
            fixed_rows = parser.parse_walk_to_rec(file_rows)
            agent_db_to_mount = "\n".join(fixed_rows)

        file_manager.mount_agent_db_for_device(dev.id, agent_db_to_mount)

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
