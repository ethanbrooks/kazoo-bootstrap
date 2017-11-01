from os.path import dirname, join, abspath

from invoke import task, Collection


BASE_PATH = abspath(join(dirname(__file__), '..'))


from . import util, tasks


collections = [tasks]

ns = Collection()
for c in collections:
    ns.add_collection(c)


ns.configure(dict(
    project='bootstrap-config',
    kazoo=dict(
        resources=['callwithus.intl', 'callwithus.us'],
        provider='voip-innovations',
        carrier_modules=['knm_voip_innovations', 'wnm_local'],
        service_plans=['test-plan-1'],
        rates_file='carrier-rates-wholesale.csv'
    ),
    paths=dict(
        base=BASE_PATH,
        config=join(BASE_PATH, 'assets', 'config'),
        data=join(BASE_PATH, 'assets', 'data')
    )
))
