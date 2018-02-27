[![License badge](https://img.shields.io/badge/license-Apache2-orange.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Docker badge](https://img.shields.io/docker/pulls/elastest/epm-adapter-docker-compose.svg)](https://hub.docker.com/r/elastests/epm-adapter-docker-compose/)

<!-- Elastest logo -->
[![][ElasTest Logo]][ElasTest]

Copyright © 2017-2019 [ElasTest]. Licensed under [Apache 2.0 License].

elastest/epm-adapter-docker-compose
==============================

What is epm-adapter-docker-compose?
==============================

The docker-compose adapter compliant to the EPM is used to launch docker-compose instances. The docker-compose file is passed along with an additional Metadata file in a package. 

# Supported tags and respective `Dockerfile` links
-	[`0.5.0` (*1.0/Dockerfile*)](https://github.com/mpauls/epm-adapter-docker-compose/blob/0.5.0/Dockerfile)
-	[`0.8.0` (*1.0/Dockerfile*)](https://github.com/mpauls/epm-adapter-docker-compose/blob/0.8.0/Dockerfile)

# Quick reference

-	**Where to get help**:  
	[the ElastTest mailing list][ElasTest Public Mailing List], [the Elastest Slack][ElasTest Slack], or [Stack Overflow][StackOverflow]

-	**Where to file issues**:  
	Issues and bug reports should be posted to the [GitHub ElasTest Bugtracker].

-	**Maintained by**:  
	[the ElasTest community](https://github.com/elastest)

-	**Published image artifact details**:
	(image metadata, transfer size, etc).

-	**Source of this description**:  
	[docs repo's `template/` directory](https://github.com/mpauls/epm-adapter-docker-compose/blob/master/docs/Docker-epm-adapter-docker-compose.md) ([history](https://github.com//mpauls/epm-adapter-docker-compose/commits/master/docs/Docker-epm-adapter-docker-compose.md))

-	**Supported Docker versions**:  
	[the latest release](https://github.com/docker/docker/releases/latest) (down to 17.03.1 on a best-effort basis)

# What's on this image?


The adapter is implemented using **python2.7** and the docker-compose, Docker and gRPC libraries.


# How to use this image


To start the adapter in a docker container run this command:
```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock -p 50051:50051 --expose 50051 -i -t epm-adapter-docker-compose
```

If you want to start both the Elastest Platform Manager and the Docker-Compose client you can use the docker-compose file below:

```bash
version: '3'
services:
    elastest-platform-manager:
        container_name: elastest-epm
        image: elastest/epm
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock:rw
        expose:
            - 8180
        ports:
            - 8180:8180
        networks:
            - elastest
    epm-adapter-docker-compose:
        container_name: elastest-epm-adapter-docker-compose
        image: elastest/epm-adapter-docker-compose
        entrypoint: python run.py --register-pop
        depends_on:
            - elastest-platform-manager
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock:rw
        expose: 
            - 50051
        ports:
            - 50051:50051
        networks:
            - elastest
networks:
    elastest:
        driver: bridge
```


This will create the docker container for both the adapter and the EPM and will also automatically register the adapter to the EPM, so you can start using them straight away.


The package has to be a **tar** file and has to have the following structure:

```bash
- Metadata.yaml #Simple metadata file that should include the name of the package
- docker-compose.yml #The docker-compose file
```

This is an example **Metadata** file:
```yaml
name: example-name
```

## Dependencies (other containers or tools)


none


## Integration with other containers or tools)


none

[Apache 2.0 License]: http://www.apache.org/licenses/LICENSE-2.0
[ElasTest]: http://elastest.io/
[ElasTest Logo]: http://elastest.io/images/logos_elastest/elastest-logo-gray-small.png
[ElasTest Twitter]: https://twitter.com/elastestio
[GitHub ElasTest Group]: https://github.com/elastest
[GitHub ElasTest Bugtracker]: https://github.com/elastest/bugtracker
[ElasTest Public Mailing List]: https://groups.google.com/forum/#!forum/elastest-users
[StackOverflow]: http://stackoverflow.com/questions/tagged/elastest
[ElasTest Slack]: elastest.slack.com
