FROM    telephoneorg/bootstrap-base:latest

MAINTAINER Joe Black <me@joeblack.nyc>

COPY    assets $HOME/assets
COPY    templates $HOME/templates
COPY    tasks $HOME/tasks

VOLUME  ["$HOME/config"]

CMD     ["inv"]
