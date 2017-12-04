from os.path import join

from invoke import task
from kzconfig import Context

from . import util


context = Context()
sup = context.sup

@task
def db_refresh(ctx):
    print(sup.kapps_maintenance.blocking_refresh())


@task
def load_resources(ctx):
    for resource in ctx.kazoo['resources']:
        print('loading resource: ', resource)
        data = util.load_config('resource.' + resource)
        print(context.kazoo.api.create_global_resource(data))
    return print(sup.sup('stepswitch_maintenance', 'reload_resources'))


@task
def load_provider(ctx):
    provider = ctx.kazoo['provider']
    print('loading provider: ', provider)
    provider_doc = util.load_config('provider.' + provider)
    print(context.couchdb.doc.create(db='system_config', doc=provider_doc))

    print(sup.kapps_config.set_json(
        'number_manager', 'carrier_modules', ctx.kazoo['carrier_modules']
    ))
    config = context.kube.api.get('secret', 'provider.' + provider).data

    print(sup.sup('ecallmgr_maintenance',
                  'allow_carrier',
                  provider,
                  config['carrier_acl']))


@task
def load_service_plans(ctx):
    master_account = context.secrets['master-account']
    db_name = context.couchdb.acct_db(master_account['id']).info()['db_name']

    for service_plan in ctx.kazoo['service_plans']:
        print('loading ', service_plan)
        doc = util.load_config('service-plan.' + service_plan)
        print(context.couchdb.doc.create(db=db_name, doc=doc))


@task
def config_authz(ctx):
    print(sup.kapps_config.set('ecallmgr', 'authz_enabled', True))
    print(sup.kapps_config.set('ecallmgr', 'authz_default_action', 'allow'))


@task(post=[config_authz])
def config_limits(ctx):
    jonny5_doc = util.load_config('jonny5')
    print(context.couchdb.doc.create(db='system_config', doc=jonny5_doc))


@task
def config_ratedeck(ctx):
    path = util.full_path(join(ctx.paths['config'], ctx.kazoo['rates_file']))
    print(context.kazoo.api.upload_ratedeck(path))


@task
def config_ecallmgr(ctx):
    print(sup.kapps_config.set('ecallmgr', 'use_kazoo_dptools', True))


@task
def config_smtp(ctx):
    smtp_doc = util.load_config('smtp-client')
    print(context.couchdb.doc.create(db='system_config', doc=smtp_doc))
    print(sup.sup('notify_maintenance', 'reload_smtp_configs'))


@task
def config_speech(ctx):
    speech_doc = util.load_config('speech')
    print(context.couchdb.doc.create(db='system_config', doc=speech_doc))
    print(sup.kapps_config.flush('speech'))


@task
def config_apps(ctx):
    master_account = context.secrets['master-account']
    print(context.kazoo.api.activate_apps(master_account['id']))


@task
def config_master_account(ctx):
    master_account = context.secrets['master-account']
    # give master-account 25000 credit
    print(sup.sup(
        'kazoo_services_maintenance',
        'credit',
        master_account['id'],
        ctx.kazoo['master_account']['credit']
    ))

    # add service-plan(s) to master-account
    print(context.kazoo.api.add_service_plans_to_account(
        master_account['id'], ctx.kazoo['service_plans']
    ))


@task
def config_crossbar(ctx):
    # setup reverse_proxy list
    addresses = ['127.0.0.1'] + util.addrs_for(*ctx.kazoo['domains'])
    print('addresses: ', addresses)
    # db = context.couchdb.api['system_config']
    # doc = db['crossbar']
    # doc['default']['reverse_proxies'] = addresses
    # db['crossbar'] = doc
    print(sup.kapps_config.set_json('crossbar', 'reverse_proxies', addresses))


# @task
# def reconfig_doodle(ctx):
#     uri = 'amqp://{}:{}@{}:5672'.format(
#         context.secrets['rabbit']['user'],
#         context.secrets['rabbit']['pass'],
#         context.configs['environment']['host.rabbitmq']
#     )
#     print('amqp uri: ', uri)
#     print(sup.kapps_config.set('doodle', 'inbound_broker', uri))


@task(pre=[db_refresh,
           load_resources,
           load_provider,
           load_service_plans,
           config_limits,
           config_ratedeck,
           config_ecallmgr,
           config_smtp,
           config_speech,
           config_apps,
           config_master_account,
           config_crossbar])
def all(ctx):
    pass
