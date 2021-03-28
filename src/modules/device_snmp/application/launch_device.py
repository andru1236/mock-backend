
from modules.shared.infrastructure import logger

from modules.device_snmp.infrastructure.command_lines import (
    exists_agent_folder,
    build_folder_for_dbs,
    run_snmpsimd_agent,
)

from modules.device_snmp.infrastructure import PATH_DBS

from modules.shared.infrastructure import process_manager


ID = "andru1236"
## TESTING
def run():
    if not exists_agent_folder():
        build_folder_for_dbs()

    # ID = "andru1236"
    PORT = 1024
    cli_process = run_snmpsimd_agent(PATH_DBS, PORT)

    def kill_process():
        cli_process.terminate()
        cli_process.kill()

    process = process_manager.Process(
        ID,
        PORT,
        [],
        cli_process,
        lambda: print(f"process already was kicked off -> PID: {cli_process.pid}"),
        kill_process # no use lamnda because it miss the context to kill the process
    )
    mgr = process_manager.ProcessManager()
    mgr.run_process(process)
    # mgr.stop_process(ID)
    
def stop():
    mgr = process_manager.ProcessManager()
    mgr.stop_process(ID)