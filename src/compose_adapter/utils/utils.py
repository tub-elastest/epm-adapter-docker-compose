import yaml
import os

def extract_metadata(tar):
    metadata = None
    for member in tar.getmembers():
        if member.name.lower() == "metadata.yaml" or member.name.lower() == "metadata.yml":
            metadata = tar.extractfile(member.name)
    if metadata is None:
        return None
    return yaml.load(metadata.read())


def extract_compose(tar, compose_path):
    compose = None
    for member in tar.getmembers():
        if member.isdir():
            os.mkdir(compose_path + "/" + member.name)
        elif member.name.lower() == "docker-compose.yaml" or member.name.lower() == "docker-compose.yml":
            compose = tar.extractfile(member.name)
        else:
            x = open(compose_path + "/" + member.name.lower(), "wb")
            x.write(tar.extractfile(member.name).read())
            x.close()
    if compose is None:
        raise Exception("No docker-compose file found in package!")
    else:
        f = open(compose_path + "/docker-compose.yml", "wb")
        f.write(compose.read())
        f.close()