from dataclasses import dataclass

from backend.shared.domain import IUseCase
from backend.shared.infrastructure import logger
from backend.device_snmp.infrastructure import snmp_object_parser


@dataclass
class FixAgentDbCommand:
    agent_db: str


class FixAgentDb(IUseCase):
    def __init__(self):
        pass

    def execute(self, command: FixAgentDbCommand):
        logger.info(f"Fixing agent db")
        parser = snmp_object_parser.SnmpObjectParser()
        
        try:
            file_rows = parser.get_fixed_rows(command.agent_db.split("\n"))
            fixed_agent_db = "\n".join(file_rows)
        except Exception as error:
            logger.error(f"There is an error when the system tried to fix the rows")
            raise error

        if fixed_agent_db == command.agent_db:
            logger.error(f"The agentdb was not changed or fixed")

        return fixed_agent_db
