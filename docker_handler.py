import docker
import os
import tarfile

from client_pb2 import ResourceGroupCompose


def convert_to_resource_group(container_ids, resource_group_name):
    client = docker.from_env()

    pops = []
    vdus = []
    networks = []

    network_names = []

    for id in container_ids:
        container = client.containers.get(id)

        name = container.attrs["Name"]
        imageName = container.attrs["Config"]["Image"]
        netName = container.attrs["HostConfig"]["NetworkMode"]
        network_names.append(netName)

        env_variables = container.attrs["Config"]["Env"]
        metadata_entries = get_inspect_as_metadata(container.attrs)
        for variable in env_variables:
            v_seperated = variable.split("=")
            # metadata_entry = models.MetadataEntryCompose(v_seperated[0], v_seperated[1])
            # metadata_entries.append(metadata_entry.to_dict())

        portBindings = container.attrs["HostConfig"]["PortBindings"]
        for key in portBindings.keys():
            for v in portBindings[key]:
                p = v["HostPort"]
                binding = p + ":" + key
                port_binding = ResourceGroupCompose.MetadataEntryCompose(key="PORT_BINDING", value=binding)
                metadata_entries.append(port_binding)

        key = next(iter(container.attrs["NetworkSettings"]["Networks"]))
        ip = container.attrs["NetworkSettings"]["Networks"][key]["IPAddress"]

        vdu = ResourceGroupCompose.VDUCompose(name=name, imageName=imageName, netName=netName, computeId=id, ip=ip,
                                              metadata=metadata_entries)
        vdus.append(vdu)

    network_names = set(network_names)
    for net_name in network_names:
        cidr = client.networks.list(names=[net_name])[0].attrs["IPAM"]["Config"][0]["Subnet"]
        netId = client.networks.list(names=[net_name])[0].attrs["Id"]
        net = ResourceGroupCompose.NetworkCompose(name=net_name, cidr=cidr, poPName="docker-local", networkId=netId)
        networks.append(net)

    rg = ResourceGroupCompose(name=resource_group_name, pops=pops, networks=networks, vdus=vdus)
    return rg


def get_inspect_as_metadata(data):
    out = list()
    for x in data:
        recursive_parsing(data, [x], out)
    return out


def recursive_parsing(data, names, out):
    a = data
    for x in names:
        a = a[x]

    if isinstance(a, unicode):
        key = names[0]
        for n in range(1, len(names)):
            key += "_" + str(names[n])
        entry = ResourceGroupCompose.MetadataEntryCompose(key=key, value=str(a).strip())
        out.append(entry)

    if isinstance(a, list) and len(a) > 0:
        if isinstance(a[0], unicode):
            value = ""
            key = names[0]
            for n in range(1, len(names)):
                key += "_" + str(names[n])
            for v in a:
                value += v + ";"
            entry = ResourceGroupCompose.MetadataEntryCompose(key=key, value=value)
            out.append(entry)
        else:
            key = names[0]
            for n in range(1, len(names)):
                key += "_" + str(names[n])
            entry = ResourceGroupCompose.MetadataEntryCompose(key=key, value=str(a).strip())
            out.append(entry)

    if isinstance(a, dict):
        for n in a:
            new_names = []
            new_names.extend(names)
            new_names.append(n)
            recursive_parsing(data, new_names, out)


def check_container_exists(container_id, all):
    client = docker.from_env()
    filters = {"id": container_id}
    found = len(client.containers.list(all=all, filters=filters))
    if found > 0:
        return True
    else:
        return False


def stop_container(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()


def start_container(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.start()


def execute_on_container(container_id, command):
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    cmd = client.exec_create(container_id, command, stdout=True, stderr=True, stdin=True)
    output = client.exec_start(cmd["Id"])
    return output


def download_file_from_container(container_id, path):
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    archive = client.get_archive(container_id, path)
    return archive[0].read()


def upload_file_to_container(container_id, path, archive):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.put_archive(path, archive)


def upload_file_to_container_from_path(container_id, hostPath, remotePath):
    # Need to find a better solution

    tar = tarfile.open(name="tmp.tar", mode="w")
    tar.add(hostPath)
    tar.close()

    f = open("tmp.tar", "rb")

    client = docker.from_env()
    container = client.containers.get(container_id)
    container.put_archive(remotePath, f.read())
    f.close()
    os.remove("tmp.tar")

    return
