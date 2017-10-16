import os

from compose.cli.main import TopLevelCommand, project_from_options
from compose.project import OneOffFilter
from operator import attrgetter


# Up the services and return the container ids
def up(project_path):
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
        "SERVICE": ""
    }

    project = project_from_options(project_path, rm_options)
    cmd = TopLevelCommand(project)
    cmd.rm(rm_options)