import yaml


def extract_metadata(tar):
    metadata = None
    for member in tar.getmembers():
        if member.name.lower() == "metadata.yaml" or member.name.lower() == "metadata.yml":
            metadata = tar.extractfile(member.name)
    if metadata is None:
        return None
    return yaml.load(metadata.read())

def extract_compose(tar):
    compose = None
    for member in tar.getmembers():
        if member.name.lower() == "docker-compose.yaml" or member.name.lower() == "docker-compose.yml":
            compose = tar.extractfile(member.name)
    if compose is None:
        return None
    return compose.read()