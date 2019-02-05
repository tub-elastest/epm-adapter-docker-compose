import grpc
import src.compose_adapter.grpc_connector.client_pb2_grpc as client_pb2_grpc
import src.compose_adapter.grpc_connector.client_pb2 as client_pb2
import time
import requests
import json
import logging
import os
import sys

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

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
                       "interfaceInfo": [{"key": "type", "value": "docker-compose"}]}

        headers = {"accept": "application/json", "content-type": "application/json"}
        headers = add_keystone_headers(headers)

        try:
            logging.info("Trying to register to EPM at: " + ip)
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
    headers = add_keystone_headers(headers)
    r = requests.delete('http://' + ip + ':8180/v1/pop/' + pop_id, headers=headers)
    logging.debug("Deleting pop resulted in: " + str(r.status_code) + " " + r.reason)


def add_keystone_headers(headers):
    if is_keystone_enabled():
        logging.debug("Keystone enabled!")
        logging.debug(get_keystone_credentials())
        keystone_endpoint, keystone_port, keystone_version, keystone_username, keystone_password, keystone_domain = get_keystone_credentials()
        auth = v3.Password(auth_url=keystone_endpoint + ":" + keystone_port + "/" + keystone_version,
                           username=keystone_username, password=keystone_password,
                           project_name=keystone_username,
                           user_domain_name=keystone_domain, project_domain_name=keystone_domain)
        sess = session.Session(auth=auth)
        keystone = client.Client(session=sess)
        try:
            keystone.authenticate(auth_url=keystone_endpoint + ":" + keystone_port + "/" + keystone_version,
                              username=keystone_username, password=keystone_password,
                              project_name=keystone_username,
                              user_domain_name=keystone_domain, project_domain_name=keystone_domain)
            headers["Authorization"] = keystone.auth_ref.auth_token
        except:
            logging.error("Unexpected error: " + str(sys.exc_info()))
    return headers

def is_keystone_enabled():
    return os.environ.get('KEYSTONE_ENABLED', 'false') == "true"


def get_keystone_credentials():
    return os.environ.get('KEYSTONE_ENDPOINT', ''), os.environ.get('KEYSTONE_PORT', ''), os.environ.get('KEYSTONE_VERSION', ''),\
           os.environ.get('KEYSTONE_USERNAME', ''), os.environ.get('KEYSTONE_PASSWORD', ''), os.environ.get('KEYSTONE_DOMAIN', '')