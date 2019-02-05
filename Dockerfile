FROM python:2.7

RUN apt-get update && apt-get install -y build-essential autoconf libtool 

RUN pip install docker-compose==1.20.0 grpcio grpcio-tools pyyaml keystoneauth1 python-keystoneclient

RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz \
  && tar xzvf docker-17.04.0-ce.tgz \
  && mv docker/docker /usr/local/bin \
  && rm -r docker docker-17.04.0-ce.tgz

ADD . docker-compose-client

WORKDIR docker-compose-client

ENTRYPOINT python run.py
