from backend.shared.infrastructure import logger
from .command_lines import (
    exists_root_folder,
    exists_db_for_device,
    build_root_folder,
    create_agent_db_folder,
    remove_agent_db_folder,
    PATH_DBS,
)


def mount_agent_db_for_device(device_guid, data_from_database):
    logger.info(f"Mounting an agent db for: {device_guid}")

    if not exists_root_folder():
        build_root_folder()

    if exists_db_for_device(device_guid):
        remove_agent_db_folder(device_guid)
        create_agent_db_folder(device_guid)
    else:
        create_agent_db_folder(device_guid)

    with open(f"{PATH_DBS}/{device_guid}/data.snmprec", "wt") as f:
        # TODO add try catch and raise Custom exception
        f.write(data_from_database)


def load_data_from_agent_db(device_guid) -> str:
    logger.info(f"Creating snapshot for device :{device_guid}")

    if not exists_root_folder() and not exists_db_for_device(device_guid):
        # TODO: create custom Exceptions
        raise Exception(f"The data was not found")

    with open(f"{PATH_DBS}/{device_guid}/data.snmprec", "rt") as f:
        data_from_file = f.read()
        return data_from_file
