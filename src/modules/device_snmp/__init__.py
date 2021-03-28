# bus of communications
from modules.shared.infrastructure import CommandBus
from .infrastructure import repository

# Features
from .application.start_simulation import StartSimulationCommand, StartSimulation
from .application.stop_simlation import StopSimulationCommand, StopSimulation


command_bus = CommandBus()

command_bus.register(
    StartSimulationCommand,
    StartSimulation(repository)
)

command_bus.register(
    StopSimulationCommand,
    StopSimulation(repository)
)