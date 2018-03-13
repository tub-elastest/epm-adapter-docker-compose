import json
import requests
import time

max_timeout = 10


def register_pop(ip, compose_ip):
    i = 0
    while i < 10:
        pop_compose = {"name": "compose-"+compose_ip,
                       "interfaceEndpoint": compose_ip,
                       "interfaceInfo":
                           [{"key": "type",
                             "value": "docker-compose"}]}

        headers = {"accept": "application/json",
                   "content-type": "application/json"}
        try:
            r = requests.post('http://' + ip + ':8180/v1/pop', data=json.dumps(pop_compose), headers=headers)
            print(str(r.status_code) + " " + r.reason)
            break
        except requests.ConnectionError:
            print("Still not connected")
        time.sleep(11)
        i += 1
