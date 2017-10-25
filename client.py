import time
import os
import tarfile

import grpc
from concurrent import futures

import client_pb2_grpc
import client_pb2
import compose_handler
import docker_handler
import yaml
import tempfile


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ComposeHandlerService(client_pb2_grpc.ComposeHandlerServicer):
    def UpCompose(self, request, context):

        default_packages_path = os.path.dirname(__file__) + "/packages"
        if not os.path.exists(default_packages_path):
            os.mkdir(default_packages_path)

        temp = tempfile.NamedTemporaryFile(delete=True)
        temp.write(request.compose_file)
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

    def RemoveCompose(self, request, context):

        compose_id = request.compose_id
        compose_path = os.path.dirname(__file__) + "/packages/" + compose_id
        compose_handler.rm(project_path=compose_path)

        os.remove(compose_path + "/docker-compose.yml")
        os.rmdir(compose_path)

        return client_pb2.Empty()


def serve(port="50051"):
    print("Starting server...")
    print("Listening on port: " + port)
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
    serve()
