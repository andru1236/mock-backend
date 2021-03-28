import subprocess, os
from modules.shared.infrastructure import logger

PATH_DBS = (os.environ.get("PATH_AGENT_DBS") or os.getcwd()) + "/AGENT_DBS"


def exists_agent_folder():
    status_code = subprocess.getstatusoutput(f"ls {PATH_DBS}")[0]
    logger.debug(f"Exists folder {PATH_DBS} -> status {status_code}")
    return True if status_code == 0 else False


def exists_db_for_device(device_guid):
    status_code = subprocess.getstatusoutput(f"ls {PATH_DBS}/{device_guid}")[0]
    logger.debug(f"Exists folder {PATH_DBS} -> status {status_code}")
    return True if status_code == 0 else False


def build_folder_for_dbs():
    if exists_agent_folder() is False:
        logger.debug(f"Creating folder in: {PATH_DBS}")
        status_code = subprocess.getstatusoutput(f"mkdir {PATH_DBS}")[0]
        logger.debug(status_code)
        return True if status_code == 0 else False
    return True
