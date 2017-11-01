from os.path import join

from invoke import task
from kzconfig import kube, kazoo, sup, couch
from kzconfig.context import context

from . import util


@task
def load_resources(ctx):
    for res in ctx.kazoo['resources']:
        print('loading ', res)
        data = util.load_config('resource.' + res)
        print(kazoo.api.create_global_resource(data))
    return print(sup.sup('stepswitch_maintenance', 'reload_resources'))


@task
def load_provider(ctx):
    provider = ctx.kazoo['provider']
    print('loading ', provider)
    provider_doc = util.load_config('provider.' + provider)
    print(couch.create_doc(db='system_config', doc=provider_doc))

    print(sup.config_set_json(
        'number_manager', 'carrier_modules', ctx.kazoo['carrier_modules']
    ))
    config = kube.api.get('secret', 'provider.' + provider).data

    print(sup.sup('ecallmgr_maintenance',
                  'allow_carrier',
                  provider,
                  config['carrier_acl']))


@task
def load_service_plans(ctx):
    master_acct_id = context.master_acct['id']
    db_name = couch.get_db_for(master_acct_id).info()['db_name']

    for sp in ctx.kazoo['service_plans']:
        print('loading ', sp)
        doc = util.load_config('service-plan.' + sp)
        print(couch.create_doc(db=db_name, doc=doc))

    # print(sup.acct_flush(master_acct_id))


@task
def config_authz(ctx):
    print(sup.config_set_default('ecallmgr', 'authz_enabled', 'true'))
    print(sup.config_set_default('ecallmgr', 'authz_default_action', 'allow'))


@task(post=[config_authz])
def config_limits(ctx):
    jonny5_doc = util.load_config('jonny5')
    print(couch.create_doc(db='system_config', doc=jonny5_doc))


@task
def config_ratedeck(ctx):
    path = util.full_path(join(ctx.paths['data'], ctx.kazoo['rates_file']))
    ok, result = kazoo.api.upload_ratedeck(path)
    print(ok, result)


@task
def config_ecallmgr(ctx):
    print(sup.config_set_default('ecallmgr', 'use_kazoo_dptools', 'true'))


@task
def config_smtp(ctx):
    smtp_doc = util.load_config('smtp-client')
    print(couch.create_doc(db='system_config', doc=smtp_doc))
    print(sup.sup('notify_maintenance', 'reload_smtp_configs'))


@task
def config_speech(ctx):
    speech_doc = util.load_config('speech')
    print(couch.create_doc(db='system_config', doc=speech_doc))
    print(sup.config_flush('speech'))


@task
def setup_master_acct(ctx):
    # give master-account 25000 credit
    print(sup.sup('kazoo_services_maintenance',
                  'credit',
                  context.master_acct['id'],
                  '25000'))

    # add service-plan(s) to master-account
    print(kazoo.api.add_service_plans_to_account(
        context.master_acct['id'],
        ctx.kazoo['service_plans']
    ))

    for app in kazoo.api.get_apps(context.master_acct['id'])['data']:
        # activating app
        print(kazoo.api.update_app(
            context.master_acct['id'],
            app['id'],
            dict(data=dict(allowed_users='all'))
        ))


@task(pre=[load_resources,
           load_provider,
           load_service_plans,
           config_limits,
           config_ratedeck,
           config_ecallmgr,
           config_smtp,
           config_speech,
           setup_master_acct])
def config(ctx):
    pass




# # init tasks
# @task(pre=[sup.db_refresh,
#            sup.create_master_account,
#            sup.import_prompts,
#            sup.init_apps,
#            add_fs_nodes,
#            allow_sbcs])
# def post_init(ctx):
#     pass
