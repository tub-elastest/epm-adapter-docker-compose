import os
import tarfile
import tempfile
import logging
from src.compose_adapter.utils import utils
from src.compose_adapter.handlers import compose_handler, docker_handler


def extract_package(request, package_path):
    default_packages_path = package_path
    if not os.path.exists(default_packages_path):
        os.mkdir(default_packages_path)

    temp = tempfile.NamedTemporaryFile(delete=True)
    temp.write(request.file)
    package = tarfile.open(temp.name, "r")

    metadata = extract_metadata(package)
    package_name = metadata.get("name")
    registry_credentials = get_registry_credentials(metadata)

    compose_path = default_packages_path + "/" + package_name
    if not os.path.exists(compose_path):
        os.mkdir(compose_path)
    utils.extract_compose(package, compose_path)

    package.close()
    temp.close()
    address, enabled = get_logging_credentials(request.metadata)

    if len(registry_credentials) == 3:
        docker_handler.login_to_registry(registry_credentials)

    container_ids = compose_handler.up(project_path=compose_path, default_logging=enabled, logging_address=address)
    return docker_handler.convert_to_resource_group(container_ids, resource_group_name=package_name)


def extract_metadata(package):
    metadata = utils.extract_metadata(package)
    if metadata is None:
        raise Exception("No metadata found in package!")
    return metadata


def get_registry_credentials(metadata):
    registry_credentials = []
    if "docker_registry" in metadata:
        if "docker_username" in metadata:
            password = ""
            if "docker_password" in metadata:
                password = metadata.get("docker_password")
            registry_credentials.append(metadata.get("docker_registry"))
            registry_credentials.append(metadata.get("docker_username"))
            registry_credentials.append(password)
        else:
            logging.error("If you specify a custom docker registry, you need to specify the login credentials.")

    return registry_credentials


def get_logging_credentials(request_metadata):
    options = request_metadata
    enabled = False
    address = ""
    for option in options:
        if option.key == "enabled":
            enabled = option.value
        if option.key == "address":
            enabled = option.value

    return enabled, address
