from os.path import join

from invoke import task


@task
def render(ctx):
    print('Rendering sensitive assets ...')
    cmd = 'tmpld --strict {}'.format(
        join(ctx.paths['templates'], ctx.assets['glob'])
    )
    print(cmd)
    print(ctx.run(cmd))


@task
def apply(ctx):
    print('Applying sensitive assets ...')
    ctx.run('kubectl apply -f {} -R'.format(ctx.paths['assets']))


@task
def delete(ctx):
    print('Applying sensitive assets ...')
    ctx.run('kubectl delete -f {} -R'.format(ctx.paths['assets']))


@task(default=True, pre=[render])
def all(ctx):
    pass
