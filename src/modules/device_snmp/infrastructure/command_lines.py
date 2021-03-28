import os
from subprocess import getstatusoutput, Popen
from modules.shared.infrastructure import logger


###################################
###### Manage folder linux  #######
###################################

PATH_DBS = (os.environ.get("PATH_AGENT_DBS") or os.getcwd()) + "/AGENT_DBS"


def exists_agent_folder():
    status_code = getstatusoutput(f"ls {PATH_DBS}")[0]
    logger.debug(f"Exists folder {PATH_DBS} -> status {status_code}")
    return True if status_code == 0 else False


def exists_db_for_device(folder_name):
    status_code = getstatusoutput(f"ls {PATH_DBS}/{folder_name}")[0]
    logger.debug(f"Check if exists folder {PATH_DBS} -> status {status_code}")
    return True if status_code == 0 else False


def create_agent_db_folder(folder_name):
    status_code = getstatusoutput(f"mkdir {PATH_DBS}/{folder_name}")[0]
    logger.debug(f"Create folder: {folder_name} in {PATH_DBS}")
    return True if status_code == 0 else False


def remove_agent_db_folder(folder_name):
    status_code = getstatusoutput(f"rm -rf {PATH_DBS}/{folder_name}")[0]
    logger.debug(f"Remove folder {folder_name} from {PATH_DBS}")
    return True if status_code == 0 else False


def build_folder_for_dbs():
    if exists_agent_folder() is False:
        logger.debug(f"Creating folder in: {PATH_DBS}")
        status_code = getstatusoutput(f"mkdir {PATH_DBS}")[0]
        logger.debug(status_code)
        return True if status_code == 0 else False
    return True


###################################
#### Manage local dependencies ####
###################################


def get_python_path():
    code, path = getstatusoutput("which python")
    logger.debug(f"path python, status code{code}, path: {path}")
    # Replace for env
    path = "/Users/andres.gutierrez/Projects/mock/mock-backend/pyenv/bin/python"
    path = os.environ.get("PYTHON_PATH") or path
    return path if path else None


def get_snmpsimd_path():
    script_name = "snmpsimd.py"
    bin_python_path = get_python_path()

    # /usr/bin/ or /bin/ or .env/bin/ -> withouy python
    binary_folder = bin_python_path[0 : len(bin_python_path) - len("/python")]

    logger.debug(f"verify is exists the script of {script_name}: {binary_folder}")

    code, path = getstatusoutput(f"ls {binary_folder}/{script_name}")
    return path if code == 0 else None


########################
####### SNMPSIMD #######
########################


def run_snmpsimd_agent(db_path, port):
    snmpsimd_script = get_snmpsimd_path()

    if snmpsimd_script is None:
        raise Exception(
            "snmpsim is not installer or there is problems to find the path"
        )

    data_param = f"--data-dir={db_path}"
    ip_and_port_param = f"--agent-udpv4-endpoint=127.0.0.1:{port}"

    cmd = [snmpsimd_script, data_param, ip_and_port_param]

    # return Popen(cmd, preexec_fn=os.setpgrp)
    return Popen(cmd)
