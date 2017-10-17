import docker

from client_pb2 import ResourceGroupCompose


def convert_to_resource_group(container_ids, resource_group_name):
    client = docker.from_env()

    pops = []
    vdus = []
    networks = []

    network_names = []

    pop = ResourceGroupCompose.PoPCompose(name="docker-local", interfaceEndpoint="unix:///var/run/docker.sock")
    pops.append(pop)

    for id in container_ids:
        container = client.containers.get(id)

        name = container.attrs["Name"]
        imageName = container.attrs["Config"]["Image"]
        netName = container.attrs["HostConfig"]["NetworkMode"]
        network_names.append(netName)

        env_variables = container.attrs["Config"]["Env"]
        metadata_entries = []
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

        vdu = ResourceGroupCompose.VDUCompose(name=name, imageName=imageName, netName=netName, computeId=id, ip=ip, metadata=metadata_entries)
        vdus.append(vdu)

    network_names = set(network_names)
    for net_name in network_names:
        cidr = client.networks.list(names=[net_name])[0].attrs["IPAM"]["Config"][0]["Subnet"]
        netId = client.networks.list(names=[net_name])[0].attrs["Id"]
        net = ResourceGroupCompose.NetworkCompose(name=net_name, cidr=cidr, poPName="docker-local", networkId=netId)
        networks.append(net)

    rg = ResourceGroupCompose(name=resource_group_name, pops=pops, networks=networks, vdus=vdus)
    return rg
