from invoke import task, Collection

from . import util, assets


namespace = Collection()
for mod in (assets,):
    namespace.add_collection(mod)


namespace.configure(dict(
    project='bootstrap-pre-init',
    paths=dict(
        base='/bootstrap',
        assets='assets',
        templates='templates',
        config='config'
    ),
    assets=dict(
        glob='**/*.j2',
        vars=['cluster.yaml']
    )
))

@task(default=True, pre=[assets.all])
def all(ctx):
    pass

namespace.add_task(all)
