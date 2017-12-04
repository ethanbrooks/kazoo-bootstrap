# Kazoo-Bootstrap
[![Build Status](https://travis-ci.org/telephoneorg/kazoo-bootstrap.svg?branch=master)](https://travis-ci.org/telephoneorg/kazoo-bootstrap) [![Docker Pulls](https://img.shields.io/docker/pulls/telephoneorg/kazoo-bootstrap.svg)](https://hub.docker.com/r/telephoneorg/kazoo-bootstrap) [![Size/Layers](https://images.microbadger.com/badges/image/telephoneorg/kazoo-bootstrap.svg)](https://microbadger.com/images/telephoneorg/kazoo-bootstrap) [![Github Repo](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/telephoneorg/kazoo-bootstrap)


## Maintainer
Joe Black | <me@joeblack.nyc> | [github](https://github.com/joeblackwaslike)


## Description
Jobs that will bootstrap a new kazoo cluster within a kubernetes cluster.


## Usage
### Under Kubernetes
#### Prereqs
* Label sbc nodes: `kubectl label node saturn.telephone.org sbc=true`.
* Label media nodes: `kubectl label node saturn.telephone.org media-server=true`.


#### Deploy
* Edit the manifests under `kubernetes/<environment>` to reflect your specific environment and configuration.
* copy, edit, and deploy ratedeck rates:
```bash
cp images/config/config/ratedeck-rates-example.csv images/config/config/ratedeck-rates.csv
vim images/config/config/ratedeck-rates.csv
docker-compose build
docker push telephoneorg/bootstrap-config:latest
```
* copy, edit, and deploy cluster configuration:
```bash
cp images/pre-init/config/cluster-example.yaml images/pre-init/config/cluster.yaml
vim images/pre-init/cluster.yaml
kubectl create secret generic cluster --from-file=images/pre-init/config/cluster.yaml
```
* Deploy the boostrap job:
```bash
kubectl apply -f `kubernetes/<environment>`
```


## Documentation
* [Rate Decks](docs/rate-decks.md)
