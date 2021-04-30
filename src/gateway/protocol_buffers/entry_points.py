from backend.shared.infrastructure import logger

from backend.device_snmp import (
    command_bus,
    StartSimulationCommand,
    StopSimulationCommand,
    FixAgentDbCommand,
)

from .generated_files import (
    simulator_services_pb2_grpc as infrastructure_simulator_services,
    simulator_services_pb2 as dto_simulator_service,
)

from .error_handler import exec_with_error_handler, ErrorResponse


command_bus.execute = exec_with_error_handler(command_bus.execute)


class SilumationService(infrastructure_simulator_services.SimulatorServicer):
    def startDeviceSimulation(self, request, context):
        logger.debug("Entry point: startDeviceSimulation")
        response = command_bus.execute(StartSimulationCommand(request.id))

        if isinstance(response, ErrorResponse):
            logger.info(f"Send response: [{response.__dict__}]")

            return dto_simulator_service.Response(
                sucessfull=response.sucessfull, message=response.message
            )

        logger.info("Sucessfull GRPC response")
        return dto_simulator_service.Response(
            sucessfull=True, message=f"The device[{request.id}] has started to run"
        )

    def stopDeviceSimulation(self, request, context):
        logger.debug("Entry point: stopDeviceSimulation")
        response = command_bus.execute(StopSimulationCommand(request.id))

        if isinstance(response, ErrorResponse):
            logger.info(f"Send response: [{response.__dict__}]")

            return dto_simulator_service.Response(
                sucessfull=response.sucessfull, message=response.message
            )
        logger.info("Sucessfull GRPC response")
        return dto_simulator_service.Response(
            sucessfull=True, message=f"The device [{request.id}] has started to run"
        )

    def fixDbAgent(self, request, context):
        logger.debug("Entry point: fixDbAgent")
        fixed_agent_db = command_bus.execute(FixAgentDbCommand(request.dbAgent))
        logger.debug("Sucessfull transformation")

        if isinstance(fixed_agent_db, ErrorResponse):
            logger.info(f"Send error response: [{fixed_agent_db.__dict__}]")
            return dto_simulator_service.Response(
                sucessfull=fixed_agent_db.sucessfull, message=fixed_agent_db.message
            )
        logger.info("Sucessfull GRPC response")
        return dto_simulator_service.DbAgent(dbAgent=fixed_agent_db)

