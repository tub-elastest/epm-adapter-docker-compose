# Elastest Platform Manager Docker-Compose client

The Docker-Compose client for the EPM is used to launch docker-compose instances. The docker-compose file is 
passed along with an additional Metadata file in a package. 

The package has to be a **tar** file and has to have the following structure:
```bash
- Metadata.yaml #Simple metadata file that should include the name of the package
- docker-compose.yml #The docker-compose file
```

This is an example **Metadata** file:
```yaml
name: example-name
```

The client is implemented using **python2.7** and the Docker-Compose, Docker and gRPC libraries.

## Launching the client

The client has to be started using the **client.py** file. The default port of the client is 50051.

## gRPC and building the protobuffers

The docker-compose client connects to the Elastic Platform Manager through gRPC. 
The protocol buffers are defined in the protos/client.proto file. There are two types defined: Messages and services. 
Messages represent the structure of the data transported using gRPC and the services represent the connection points.

There are two ways to build the modules for the python client :

1) Using the protocol buffer from python (for proto3 use python 2.7)

```bash
python -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/client.proto
```

2) Installing the protocol buffer : https://github.com/grpc/grpc/blob/master/INSTALL.md

### Defining the proto file

This is the guide for defining **proto3** files: https://developers.google.com/protocol-buffers/docs/proto3

This is an example of a **proto3** file: https://github.com/grpc/grpc/blob/v1.6.x/examples/protos/route_guide.proto 

### Using the generated modules

This is an example of creating client / server code : https://grpc.io/docs/tutorials/basic/python.html