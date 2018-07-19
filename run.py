import os
import sys
import time
import logging
from logging import handlers
import atexit

import grpc
import src.compose_adapter.grpc_connector.client_pb2_grpc as client_pb2_grpc
from concurrent import futures

import src.compose_adapter.grpc_connector.client_pb2 as client_pb2
from src.compose_adapter.utils import epm_utils, utils
from src.compose_adapter.handlers import compose_handler, docker_handler, package_handler

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

packages_path = os.path.dirname(__file__) + "/packages"

class ComposeHandlerService(client_pb2_grpc.OperationHandlerServicer):
    def Create(self, request, context):

        return package_handler.extract_package(request, packages_path)

    def CheckStatus(self, request, context):
        """
        Status:
        0 - CONFIGURING
        1 - ACTIVE
        2 - INACTIVE
        """
        return client_pb2.Status(status=1)

    def CheckIfContainerExists(self, request, context):

        compose_id = request.resource_id
        result = str(docker_handler.check_container_exists(compose_id, True))
        return client_pb2.StringResponse(response=result)

    def CheckIfContainerRunning(self, request, context):

        compose_id = request.resource_id
        result = str(docker_handler.check_container_exists(compose_id, False))
        return client_pb2.StringResponse(response=result)

    def Remove(self, request, context):

        compose_id = request.resource_id
        compose_path = os.path.dirname(__file__) + "/packages/" + compose_id
        compose_handler.rm(project_path=compose_path)

        utils.clean_folder(compose_path)

        return client_pb2.Empty()

    def Start(self, request, context):

        container_id = request.resource_id
        logging.info("Starting container " + container_id)
        docker_handler.start_container(container_id)
        return client_pb2.Empty()

    def Stop(self, request, context):
        container_id = request.resource_id
        logging.info("Stopping container " + container_id)
        docker_handler.stop_container(container_id)
        return client_pb2.Empty()

    def ExecuteCommand(self, request, context):
        container_id = request.vdu.computeId
        command = request.property[0]
        logging.info("Executing command " + command)
        output = docker_handler.execute_on_container(container_id, command)
        return client_pb2.StringResponse(response=output)

    def DownloadFile(self, request, context):
        container_id = request.vdu.computeId
        path = request.property[0]
        logging.info("Downloading file " + path)
        output = docker_handler.download_file_from_container(container_id, path)
        return client_pb2.FileMessage(file=output)

    def UploadFile(self, request, context):

        container_id = request.vdu.computeId
        type = request.property[0]
        if type == "withPath":
            remotePath = request.property[2]
            hostPath = request.property[1]
            logging.info("Uploading a file " + hostPath + " to " + remotePath)
            docker_handler.upload_file_to_container_from_path(container_id, hostPath, remotePath)
            return client_pb2.Empty()
        else:
            path = request.property[0]
            logging.info("Uploading a file to " + path)
            file = request.file
            docker_handler.upload_file_to_container(container_id, path, file)
            return client_pb2.Empty()



def serve(port="50051"):
    logging.info("Starting server...")
    logging.info("Listening on port: " + port)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_OperationHandlerServicer_to_server(
        ComposeHandlerService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

adapter_id = ""
epm_ip = ""

@atexit.register
def stop():
    logging.info("Exiting")
    if adapter_id != "" and epm_ip != "":
        logging.info("DELETING ADAPTER")
        epm_utils.unregister_adapter(epm_ip, adapter_id)


if __name__ == '__main__':
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    log.addHandler(ch)

    fh = handlers.RotatingFileHandler("compose-adapter-ansible.log", maxBytes=(1048576 * 5), backupCount=7)
    fh.setFormatter(format)
    log.addHandler(fh)
    logging.info("\n")

    if "--register-adapter" in sys.argv:
        if len(sys.argv) == 4:
            logging.info("Trying to register pop to EPM container...")
            adapter_id = epm_utils.register_adapter(ip=sys.argv[2], compose_ip=sys.argv[3])
            epm_ip = sys.argv[2]
        else:
            ip = "elastest-epm"
            compose_ip = "elastest-epm-adapter-docker-compose"
            adapter_id = epm_utils.register_adapter(ip=ip, compose_ip=compose_ip)
            epm_ip = ip
    serve()
