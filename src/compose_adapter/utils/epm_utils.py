import grpc
import src.compose_adapter.grpc_connector.client_pb2_grpc as client_pb2_grpc
import src.compose_adapter.grpc_connector.client_pb2 as client_pb2
import time

max_timeout = 10

def register_adapter(ip, compose_ip):
    channel = grpc.insecure_channel(ip+":50050")
    stub = client_pb2_grpc.AdapterHandlerStub(channel)

    endpoint = compose_ip + ":50051"
    adapter = client_pb2.AdapterProto(type="docker-compose", endpoint=endpoint)

    i = 0
    while i < 10:
        try:
            stub.RegisterAdapter(adapter)
            print("Adapter registered")
            break
        except :
            print("Still not connected")
        time.sleep(11)
        i += 1
