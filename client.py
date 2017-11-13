import time
import os
import sys
import tarfile

import grpc
from concurrent import futures

import client_pb2_grpc
import client_pb2
import compose_handler
import docker_handler
import yaml
import tempfile
import epm_utils

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ComposeHandlerService(client_pb2_grpc.ComposeHandlerServicer):
    def UpCompose(self, request, context):

        default_packages_path = os.path.dirname(__file__) + "/packages"
        if not os.path.exists(default_packages_path):
            os.mkdir(default_packages_path)

        temp = tempfile.NamedTemporaryFile(delete=True)
        temp.write(request.file)
        package = tarfile.open(temp.name, "r")

        metadata = yaml.load(package.extractfile("metadata.yaml").read())
        package_name = metadata.get("name")

        compose_path = os.path.dirname(__file__) + "/packages/" + package_name
        if not os.path.exists(compose_path):
            os.mkdir(compose_path)

        f = open(os.path.dirname(__file__) + "/packages/" + package_name + "/docker-compose.yml", "wb")
        f.write(package.extractfile("docker-compose.yml").read())
        f.close()
        package.close()
        temp.close()

        container_ids = compose_handler.up(project_path=compose_path)
        rg = docker_handler.convert_to_resource_group(container_ids, resource_group_name=package_name)
        return rg

    def CheckIfContainerExists(self, request, context):

        compose_id = request.resource_id
        result = str(docker_handler.check_container_exists(compose_id, True))
        return client_pb2.StringResponse(response=result)

    def CheckIfContainerRunning(self, request, context):

        compose_id = request.resource_id
        result = str(docker_handler.check_container_exists(compose_id, False))
        return client_pb2.StringResponse(response=result)

    def RemoveCompose(self, request, context):

        compose_id = request.resource_id
        compose_path = os.path.dirname(__file__) + "/packages/" + compose_id
        compose_handler.rm(project_path=compose_path)

        os.remove(compose_path + "/docker-compose.yml")
        os.rmdir(compose_path)

        return client_pb2.Empty()

    def StartContainer(self, request, context):
        container_id = request.resource_id
        print("Starting container " + container_id)
        docker_handler.start_container(container_id)
        return client_pb2.Empty()

    def StopContainer(self, request, context):
        container_id = request.resource_id
        print("Stopping container " + container_id)
        docker_handler.stop_container(container_id)
        return client_pb2.Empty()

    def ExecuteCommand(self, request, context):
        container_id = request.resource_id
        command = request.property
        print("Executing command " + command)
        output = docker_handler.execute_on_container(container_id, command)
        return client_pb2.StringResponse(response=output)

    def DownloadFile(self, request, context):
        container_id = request.resource_id
        path = request.property
        print("Downloading file " + path)
        output = docker_handler.download_file_from_container(container_id, path)
        return client_pb2.FileMessage(file=output)

    def UploadFile(self, request, context):
        container_id = request.resource_id
        path = request.property
        print("Uploading a file to " + path)
        file = request.file
        docker_handler.upload_file_to_container(container_id, path, file)
        return client_pb2.Empty()


def serve(port="50051", register=False):
    print("Starting server...")
    print("Listening on port: " + port)

    if register:
        print("Trying to register pop to EPM container...")
        epm_utils.register_pop()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_ComposeHandlerServicer_to_server(
        ComposeHandlerService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    if "--register-pop" in sys.argv:
        serve(register=True)
    else:
        serve()
