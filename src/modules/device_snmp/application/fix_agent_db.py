from dataclasses import dataclass

from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger
from modules.device_snmp.infrastructure import snmp_object_parser


@dataclass
class FixAgentDbCommand:
    agent_db: str


class FixAgentDb(IUseCase):
    def __init__(self):
        pass

    def execute(self, command: FixAgentDbCommand) -> None:
        logger.info(f"Fixing agent db")
        parser = snmp_object_parser.SnmpObjectParser()

        try:
            fixed_agent_db = parser.get_fixed_rows(command.agent_db)
        except Exception as error:
            logger.error(f"There is an error when the system tried to fix the rows")
            raise error

        return fixed_agent_db
