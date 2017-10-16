import unittest
import grpc

import client_pb2
import client_pb2_grpc


class TestClient(unittest.TestCase):

    def test_up_compose(self):
        channel = grpc.insecure_channel("localhost:50051")
        stub = client_pb2_grpc.ComposeHandlerStub(channel)

        f = open("compose-package.tar", "rb")
        dc = client_pb2.ComposePackage(compose_file=f.read())
        f.close()
        rg = stub.UpCompose(dc)
        print(rg)

        id = client_pb2.ComposeIdentifier(compose_id="test-package")
        stub.RemoveCompose(id)

        return

if __name__ == "__main__":

    unittest.main()