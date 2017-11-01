from os.path import dirname, join, abspath

from invoke import task
from kzconfig import kube, kazoo, sup, couch, util
from kzconfig.context import context


BASE_PATH = abspath(join(dirname(__file__), '..'))


@task
def db_refresh(ctx):
    print(sup.db_refresh())

@task
def create_master_account(ctx):
    master_acct = context.master_acct
    print(sup.sup('crossbar_maintenance',
                  'create_account',
                  master_acct['name'],
                  master_acct['realm'],
                  master_acct['user'],
                  util.quote(master_acct['pass'])
    ))


@task
def import_prompts(ctx):
    env = context.env
    print(sup.sup('kazoo_media_maintenance',
                  'import_prompts',
                  env['path.media'],
                  env['language']
    ))


@task
def init_apps(ctx):
    env = context.env
    print(sup.sup('crossbar_maintenance',
                  'init_apps',
                  env['path.monster-apps'],
                  env['uri.crossbar']
    ))


@task
def add_fs_nodes(ctx):
    ep = kube.api.get('endpoint', 'freeswitch')
    print('adding media servers')

    for node in ep.nodes:
        print('adding fs_node: ', node)
        print(sup.sup('ecallmgr_maintenance',
                      'add_fs_node',
                      'freeswitch@' + node
        ))


@task
def allow_sbcs(ctx):
    ep = kube.api.get('endpoint', 'kamailio')
    print('adding sbcs')

    for addr in ep.addresses:
        ip = addr.target['status']['hostIP']
        host = addr.target['spec']['nodeName']
        print('adding sbc: ', host, ip)
        print(sup.sup('ecallmgr_maintenance',
                      'allow_sbc',
                      host,
                      ip
        ))


@task
def get_api_creds(ctx):
    db = couch.api['system_config']
    doc = db['accounts']
    acct_id = doc['default']['master_account_id']

    db = couch.api['accounts']
    doc = db[acct_id]
    api_key = doc['pvt_api_key']

    master_acct = kube.api.get('secret', 'master-account')
    master_acct._wrapper.obj['data'].update({
        'id': util.b64encode(acct_id),
        'api-key': util.b64encode(api_key)
    })
    master_acct._wrapper.update()


@task
def enable_sup_api(ctx):
    print(sup.sup('crossbar_maintenance',
                  'start_module',
                  'cb_sup'
    ))


@task(pre=[db_refresh,
           create_master_account,
           import_prompts,
           init_apps,
           add_fs_nodes,
           allow_sbcs,
           get_api_creds,
           enable_sup_api])
def post_init(ctx):
    pass
