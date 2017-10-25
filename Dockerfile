FROM python:3


RUN apt-get update && apt-get install -y build-essential autoconf libtool 

RUN pip install docker-compose grpcio grpcio-tools

ADD . docker-compose-client

WORKDIR docker-compose-client

RUN python -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/client.proto

ENTRYPOINT python client.py
