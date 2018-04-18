import grpc
import src.compose_adapter.grpc_connector.client_pb2_grpc as client_pb2_grpc
import src.compose_adapter.grpc_connector.client_pb2 as client_pb2
import time
import requests
import json

max_timeout = 10


def register_adapter(ip, compose_ip):
    channel = grpc.insecure_channel(ip + ":50050")
    stub = client_pb2_grpc.AdapterHandlerStub(channel)
    endpoint = compose_ip + ":50051"
    adapter = client_pb2.AdapterProto(type="docker-compose", endpoint=endpoint)

    i = 0
    while i < 10:
        pop_compose = {"name": "compose-" + compose_ip,
                       "interfaceEndpoint": compose_ip,
                       "interfaceInfo":[{"key": "type","value": "docker-compose"}]}

        headers = {"accept": "application/json","content-type": "application/json"}
        try:
            identifier = stub.RegisterAdapter(adapter)
            r = requests.post('http://' + ip + ':8180/v1/pop', data=json.dumps(pop_compose), headers=headers)
            print("Adapter registered")
            print(str(r.status_code) + " " + r.reason)
            return identifier.resource_id
        except:
            print("Still not connected")
        time.sleep(11)
        i += 1
    return ""


def unregister_adapter(ip, id):
    channel = grpc.insecure_channel(ip + ":50050")
    stub = client_pb2_grpc.AdapterHandlerStub(channel)
    identifier = client_pb2.ResourceIdentifier(resource_id=id)
    stub.DeleteAdapter(identifier)
