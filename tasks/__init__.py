import os

from invoke import task, Collection

from . import test, dc, kube, hub


collections = [test, dc, kube, hub]

ns = Collection()
for c in collections:
    ns.add_collection(c)

ns.configure(dict(
    project='bootstrap-jobs',
    repo='docker-bootstrap-jobs',
    pwd=os.getcwd(),
    docker=dict(
        user=os.getenv('DOCKER_USER', 'joeblackwaslike'),
        org=os.getenv('DOCKER_ORG', 'telephoneorg'),
        name='kube-bootstrap',
        tag='latest',
        images=['bootstrap-base', 'bootstrap-pre-init', 'bootstrap-post-init', 'bootstrap-config'],
        shell='bash'
    ),
    kube=dict(
        cluster_file='images/pre-init/config/cluster.yaml'
    )
))
