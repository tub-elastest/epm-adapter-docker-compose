import unittest
import grpc
import tarfile
import io

import client_pb2
import client_pb2_grpc


class TestClient(unittest.TestCase):

    def test_runtime_full(self):
        channel = grpc.insecure_channel("localhost:50051")
        stub = client_pb2_grpc.ComposeHandlerStub(channel)

        f = open("compose-package.tar", "rb")
        dc = client_pb2.FileMessage(file=f.read())
        f.close()
        rg = stub.UpCompose(dc)

        print(rg)

        container_id = rg.vdus[0].computeId
        # Stop container
        r_id = client_pb2.ResourceIdentifier(resource_id=container_id)
        stub.StopContainer(r_id)

        # Start container
        stub.StartContainer(r_id)

        # Upload file
        f = open("compose-package.tar", "rb")
        upld_message = client_pb2.DockerRuntimeMessage(resource_id=container_id, property=["/"], file=f.read())
        stub.UploadFile(upld_message)
        f.close()

        #Upload file using path
        upld_message_with_path = client_pb2.DockerRuntimeMessage(resource_id=container_id, property=["withPath","README.md", "/"])
        stub.UploadFile(upld_message_with_path)

        # Execute command
        cmd = client_pb2.DockerRuntimeMessage(resource_id=container_id, property=["ls"], file=None)
        response_string = stub.ExecuteCommand(cmd)
        print(response_string.response)

        # Download file
        dwnld_message = client_pb2.DockerRuntimeMessage(resource_id=container_id, property=["/metadata.yaml"], file=None)
        output = stub.DownloadFile(dwnld_message)
        file_like = io.BytesIO(output.file)
        archive = tarfile.open(fileobj=file_like, mode="r")
        print(archive.extractfile("metadata.yaml").read())
        archive.close()

        # Down compose
        id = client_pb2.ResourceIdentifier(resource_id="test-package")
        stub.RemoveCompose(id)


if __name__ == "__main__":
    unittest.main()
