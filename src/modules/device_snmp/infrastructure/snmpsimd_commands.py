from subprocess import getstatusoutput
from modules.shared.infrastructure import logger


def get_python_path():
    code, path = getstatusoutput("which python")
    logger.debug(f"path python, status code{code}, path: {path}")
    return path if path else None


def is_snmpsimd_installed(script_name="snmpsimd.py"):
    bin_python_path = get_python_path()
    snmpsimd_path = bin_python_path[
        0 : len(bin_python_path) - len("/python")
    ]  # get binary folders of python
    logger.debug(f"verify is exists the script of {script_name}: {snmpsimd_path}")
    code = getstatusoutput(f"ls {snmpsimd_path}/{script_name}")[0]
    return True if code == 0 else False
