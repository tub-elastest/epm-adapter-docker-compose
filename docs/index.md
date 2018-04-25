# Elastest Platform Manager Docker-Compose adapter

The Docker-Compose adapter compliant with ElasTest Platform Manager is used to launch docker-compose instances. The docker-compose file is passed along with an additional Metadata file in a package. 

The package has to be a **tar** file and has to have the following structure:
```bash
- Metadata.yaml #Simple metadata file that should include the name of the package
- docker-compose.yml #The docker-compose file
```

This is an example **Metadata** file:
```yaml
name: example-name
```

The adapter is implemented using **python2.7** and the Docker-Compose, Docker and gRPC libraries.

## Launching the adapter

The adapter has to be started using the **run.py** file. The default port of the adapter is 50051.

```bash
python -m run
```

If the EPM is already running you can make the adapter register itself on the EPM automatically and 
you won't need to register a pop manually.

```yaml
python run.py --register-adapter <epm-ip> <compose-adapter-ip>

```

## Launching the adapter in a docker container

To start the adapter in a docker container run this command:
```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock -p 50051:50051 --expose 50051 -i -t elastest/epm-adapter-docker-compose
```

## Launching the adapter and the EPM in a docker containers

If you want to start both the Elastest Platform Manager and the Docker-Compose adapter you can run:

```bash
docker-compose up
```

This will create the docker container for both the adapter and the EPM and will also automatically register 
the adapter to the EPM, so you can start using them straight away.


## Usage

The Docker Compose Adapter is built to be able to work only on the local docker compose environment, due to the 
way that docker compose itself is built. Therefore when registering the adapter will also register a pop for the 
docker compose environment that it can reach, so no further configurations are needed before launching packages.
