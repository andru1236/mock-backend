import os
import grpc
from concurrent import futures
from backend.shared.infrastructure import logger

from .generated_files import simulator_services_pb2_grpc as infrastructure_simulator_services
from .entry_points import SilumationService


PORT = os.environ.get('GRPC_PORT') or 5001


def start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    infrastructure_simulator_services.add_SimulatorServicer_to_server(
        SilumationService(), server
    )
    logger.info(f"Starting run the server GRPC in port: {PORT}")
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    logger.info("The GRPC is running sucessfull")
    server.wait_for_termination()
