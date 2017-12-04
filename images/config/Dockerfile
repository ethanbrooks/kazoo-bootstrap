FROM    telephoneorg/bootstrap-base:latest

MAINTAINER Joe Black <me@joeblack.nyc>

VOLUME  ["$HOME/templates", "$HOME/config"]

COPY    assets $HOME/assets
COPY    templates $HOME/templates
COPY    config $HOME/config
COPY    tasks $HOME/tasks

CMD     ["inv"]
