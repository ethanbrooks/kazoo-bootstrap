from os.path import dirname, join, abspath

from invoke import task, Collection

from . import util, assets, kazoo


namespace = Collection()
for mod in [assets, kazoo]:
    namespace.add_collection(mod)


namespace.configure(dict(
    project='bootstrap-config',
    kazoo=dict(
        resources=['callwithus-intl', 'callwithus-us'],
        provider='voip-innovations',
        dns='dnsimple',
        carrier_modules=['knm_voip_innovations', 'knm_local'],
        service_plans=['test-plan-1'],
        rates_file='ratedeck-rates.csv',
        domains=['cluster.telephone.org', 'cluster.local.telephone.org'],
        master_account=dict(
            credit='25000'
        )
    ),
    assets=dict(
        glob='*.j2',
    ),
    paths=dict(
        base='/bootstrap',
        assets='assets',
        templates='templates',
        config='config'
    )
))

@task(default=True, pre=[assets.all, kazoo.all])
def all(ctx):
    pass

namespace.add_task(all)
