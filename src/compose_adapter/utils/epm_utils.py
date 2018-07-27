import grpc
import src.compose_adapter.grpc_connector.client_pb2_grpc as client_pb2_grpc
import src.compose_adapter.grpc_connector.client_pb2 as client_pb2
import time
import requests
import json
import logging

max_timeout = 10


def register_adapter(ip, compose_ip):
    pop_id = ""
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
            logging.info("Adapter registered")
            logging.debug(str(r.status_code) + " " + r.reason)
            logging.debug(r.json())
            pop_id = r.json()["id"]

            return identifier.resource_id, pop_id
        except:
            logging.debug("Still not connected")
        time.sleep(11)
        i += 1
    return "", pop_id


def unregister_adapter(ip, adapter_id, pop_id):
    channel = grpc.insecure_channel(ip + ":50050")
    stub = client_pb2_grpc.AdapterHandlerStub(channel)
    identifier = client_pb2.ResourceIdentifier(resource_id=adapter_id)
    stub.DeleteAdapter(identifier)

    headers = {"accept": "application/json", "content-type": "application/json"}
    r = requests.delete('http://' + ip + ':8180/v1/pop/' + pop_id, headers=headers)
    logging.debug("Deleting pop resulted in: " + str(r.status_code) + " " + r.reason)
