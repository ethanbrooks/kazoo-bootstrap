from os.path import join

from invoke import task
from kzconfig.util import to_str


@task
def render(ctx):
    print('Rendering sensitive assets ...')
    cmd = 'tmpld --strict {} {}'.format(
        to_str(ctx.assets['vars'], path=ctx.paths['config']),
        join(ctx.paths['templates'], ctx.assets['glob'])
    )
    ctx.run(cmd)


@task
def apply(ctx):
    print('Applying sensitive assets ...')
    ctx.run('kubectl apply -f {} -R'.format(ctx.paths['assets']))


@task
def delete(ctx):
    print('Applying sensitive assets ...')
    ctx.run('kubectl delete -f {} -R'.format(ctx.paths['assets']))


@task(default=True, pre=[render, apply])
def all(ctx):
    pass
