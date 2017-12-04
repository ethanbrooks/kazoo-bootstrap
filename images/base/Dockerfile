FROM    telephoneorg/kzutil:latest

MAINTAINER Joe Black <me@joeblack.nyc>

ENV     HOME=/bootstrap

ENV     LC_ALL=C.UTF-8
ENV     LANG=C.UTF-8

RUN     mkdir -p $HOME/.kube

WORKDIR $HOME

COPY    words /usr/share/dict/

RUN     apt-get update -qq && \
            apt-get install -yqq \
                ca-certificates \
                curl \
                jq \
                python3 \
                python3-pip && \
            apt-clean --aggressive

RUN     pip3 install --upgrade pip requests setuptools

RUN     pip3 install invoke

ARG     TMPLD_VERSION
ENV     TMPLD_VERSION=${TMPLD_VERSION:-0.2.9}
RUN     pip3 install tmpld==$TMPLD_VERSION

ARG     KZCONFIG_VERSION
ENV     KZCONFIG_VERSION=${KZCONFIG_VERSION:-0.3.2}
RUN     pip3 install kzconfig==$KZCONFIG_VERSION

ARG     KUBECTL_VERSION
ARG     KUBECTL_SHA256

ENV     KUBECTL_VERSION=${KUBECTL_VERSION:-1.7.8}
ENV     KUBECTL_SHA256=${KUBECTL_SHA256:-c4fd350f9fac76121dda479c1ceba2d339b19f8806aa54207eff55c9c6896724}

RUN     install-kubectl

ENV     TMPLD_LOG_LEVEL INFO
