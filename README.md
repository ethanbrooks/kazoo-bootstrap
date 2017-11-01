# Kazoo-Bootstrap
[![Build Status](https://travis-ci.org/telephoneorg/kazoo-bootstrap.svg?branch=master)](https://travis-ci.org/telephoneorg/kazoo-bootstrap) [![Docker Pulls](https://img.shields.io/docker/pulls/telephoneorg/kazoo-bootstrap.svg)](https://hub.docker.com/r/telephoneorg/kazoo-bootstrap) [![Size/Layers](https://images.microbadger.com/badges/image/telephoneorg/kazoo-bootstrap.svg)](https://microbadger.com/images/telephoneorg/kazoo-bootstrap) [![Github Repo](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/telephoneorg/kazoo-bootstrap)


## Maintainer
Joe Black | <me@joeblack.nyc> | [github](https://github.com/joeblackwaslike)


## Description
Jobs that will bootstrap a new kazoo cluster within a kubernetes cluster.


## Usage
### Under Kubernetes
* Edit the manifests under `kubernetes/<environment>` to reflect your specific environment and configuration.
* Deploy the boostrap job:
```bash
kubectl create -f `kubernetes/<environment>`
```
