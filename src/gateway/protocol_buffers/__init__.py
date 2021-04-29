import grpc
from concurrent import futures

from .generated_files import (
    simulator_services_pb2_grpc as infrastructure_simulator_services,
    simulator_services_pb2 as dto_simulator_service,
)

from backend.api_instance import query_bus, SearchApiQuery
from backend.shared.infrastructure import logger


class SilumationService(infrastructure_simulator_services.SimulatorServicer):
    def startDeviceSimulation(self, request, context):
        logger.info("GRPC started device simulation")
        response = query_bus.execute(SearchApiQuery(request.id))
        logger.info(f"Response:\n {response}")  
        return dto_simulator_service.Response(sucessfull=True, message=str(response))


def start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    infrastructure_simulator_services.add_SimulatorServicer_to_server(
        SilumationService(), server
    )
    server.add_insecure_port("[::]:5001")
    server.start()
    server.wait_for_termination()
