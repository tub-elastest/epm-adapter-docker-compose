# Elastest Platform Manager Docker-Compose adapter

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

```bash
python run.py
```

If the EPM is already running you can make the client register itself on the EPM automatically and 
you won't need to register a pop manually.

```yaml
python run.py --register-pop <epm-ip> <compose-client-ip>

```

## Launching the client in a docker container

To start the client in a docker container run this command:
```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock -p 50051:50051 --expose 50051 -i -t epm-compose-client
```

## Launching the client and the EPM in a docker containers

If you want to start both the Elastest Platform Manager and the Docker-Compose client you can run:

```bash
docker-compose up
```

This will create the docker container for both the client and the EPM and will also automatically register 
the client to the EPM, so you can start using them straight away.
