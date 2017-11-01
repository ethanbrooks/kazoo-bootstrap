FROM    telephoneorg/bootstrap-base:latest

MAINTAINER Joe Black <me@joeblack.nyc>

ARG     KZCONFIG_VERSION
ENV     KZCONFIG_VERSION ${KZCONFIG_VERSION:-0.2.0}

RUN     pip3 install invoke kzconfig==$KZCONFIG_VERSION

COPY    entrypoint /
COPY    assets /assets
COPY    tasks /tasks
COPY    templates /templates

CMD     ["/entrypoint"]
