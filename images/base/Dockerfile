FROM    telephoneorg/debian:stretch

MAINTAINER Joe Black <me@joeblack.nyc>

ARG     TMPLD_VERSION
ARG     KUBERNETES_VERSION

ENV     HOME=/bootstrap

RUN     mkdir -p $HOME/.kube
COPY    config $HOME/.kube/
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

ENV     KUBERNETES_VERSION=${KUBERNETES_VERSION:-1.7.3}

RUN     curl -Lo /usr/local/bin/kubectl \
            https://storage.googleapis.com/kubernetes-release/release/v${KUBERNETES_VERSION}/bin/linux/amd64/kubectl && \
        chmod +x /usr/local/bin/kubectl

ENV     TMPLD_VERSION=${TMPLD_VERSION:-0.2.7}
RUN     pip3 install tmpld==$TMPLD_VERSION

ENV     TMPLD_LOG_LEVEL INFO
