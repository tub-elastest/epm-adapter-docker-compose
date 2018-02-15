import os

from compose.cli.main import TopLevelCommand, project_from_options
from compose.project import OneOffFilter
from operator import attrgetter
import yaml


# Up the services and return the container ids
def up(project_path, default_logging):
    if default_logging:
        set_logging_driver(project_path)

    up_options = {"-d": True,
                  "--no-color": False,
                  "--no-deps": False,
                  "--build": False,
                  "--abort-on-container-exit": False,
                  "--remove-orphans": False,
                  "--no-recreate": True,
                  "--force-recreate": False,
                  "--no-build": False,
                  "SERVICE": "",
                  "--scale": []
                  }

    project = project_from_options(project_path, up_options)
    cmd = TopLevelCommand(project)
    cmd.up(up_options)

    ps_options = {
        "SERVICE": "",
        "-q": True
    }
    containers = sorted(
        project.containers(service_names=ps_options['SERVICE'], stopped=True) +
        project.containers(service_names=ps_options['SERVICE'], one_off=OneOffFilter.only),
        key=attrgetter('name'))

    container_ids = []
    for container in containers:
        container_ids.append(container.id)

    return container_ids


def rm(project_path):
    rm_options = {
        "--force": True,
        "--stop": True,
        "-v": False,
        "--rmi": "none",
        "--volumes": "/private",
        "--remove-orphans": False,
        "SERVICE": ""
    }

    project = project_from_options(project_path, rm_options)
    cmd = TopLevelCommand(project)
    cmd.down(rm_options)


def set_logging_driver(project_path):
    f = open(project_path + "/docker-compose.yml", "r")
    compose = yaml.load(f.read())
    f.close()
    for service in compose["services"]:
        if not compose["services"][service].has_key("logging"):
            f = open(project_path + "/docker-compose.yml", "w")
            default_driver = {'driver': 'syslog', 'options': {'syslog-address': 'tcp://localhost:5000'}}
            compose["services"][service]['logging'] = default_driver
            yaml.dump(compose, f, default_flow_style=False)
            f.close()
