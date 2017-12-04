from invoke import task, Collection

from . import util, sup


namespace = Collection()
for mod in (sup,):
    namespace.add_collection(mod)


namespace.configure(dict(
    project='bootstrap-post-init',
    paths=dict(
        base='/bootstrap'
    ),
    kazoo=dict(
        crossbar_modules=[
            'alerts'
            'call_inspector',
            'dialplans',
            'multi_factor',
            'security',
            'storage'
            'sup'
        ],
        sbc_selector={'sbc': 'true'},
        media_server_selector={'media-server': 'true'}
    )
))

@task(default=True, pre=[sup.all])
def all(ctx):
    pass

namespace.add_task(all)
