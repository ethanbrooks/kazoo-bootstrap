FROM    telephoneorg/bootstrap-base:latest

MAINTAINER Joe Black <me@joeblack.nyc>

COPY    entrypoint /
COPY    assets /assets
COPY    templates /templates

CMD     ["/entrypoint"]

VOLUME  ["/config"]
