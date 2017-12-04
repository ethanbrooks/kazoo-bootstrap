from invoke import task

from kzconfig.util import to_str, quote, b64encode
from kzconfig import Context


context = Context()
env = context.configs['environment']

# helpers
def store_api_creds():
    db = context.couchdb.api['system_config']
    doc = db['accounts']
    acct_id = doc['default']['master_account_id']

    db = context.couchdb.api['accounts']
    doc = db[acct_id]
    api_key = doc['pvt_api_key']

    master_acct = context.kube.api.get('secret', 'master-account')
    master_acct._wrapper.obj['data'].update({
        'id': b64encode(acct_id),
        'api-key': b64encode(api_key)
    })
    master_acct._wrapper.update()


@task
def db_refresh(ctx):
    print('Refreshing database')
    ctx.run('sup kapps_maintenance refresh')


@task
def create_master_account(ctx):
    master_account = context.secrets['master-account']
    ctx.run("sup crossbar_maintenance create_account {} {} {} {}".format(
        master_account['name'],
        master_account['realm'],
        master_account['user'],
        quote(master_account['pass'])
    ))
    store_api_creds()

@task
def import_prompts(ctx):
    print('Importing prompts')
    ctx.run('sup kazoo_media_maintenance import_prompts {} {}'.format(
        env['path.media'], env['language']
    ))


@task
def init_apps(ctx):
    print('Initializing monster apps ...')
    ctx.run('sup crossbar_maintenance init_apps {} {}'.format(
         env['path.monster-apps'], env['uri.crossbar']
    ))


@task
def add_media_servers(ctx):
    print('adding media servers ...')
    nodes = context.kube.api.get(
        'node', namespace=None, selector=ctx.kazoo['media_server_selector'])
    for node in nodes:
        ctx.run('sup ecallmgr_maintenance add_fs_node {}'.format(
            'freeswitch@' + node.hostname
        ))


@task
def allow_sbcs(ctx):
    print('adding sbc acls ...')
    nodes = context.kube.api.get(
        'node', namespace=None, selector=ctx.kazoo['sbc_selector'])
    for node in nodes:
        ctx.run('sup ecallmgr_maintenance allow_sbc {} {}'.format(
            node.ip, node.hostname
        ))

@task
def enable_crossbar_mods(ctx):
    print('enabling crossbar modules ...')
    for mod in ctx.kazoo['crossbar_modules']:
        ctx.run('sup crossbar_maintenance start_module cb_{}'.format(mod))


@task(default=True,
      pre=[db_refresh,
           create_master_account,
           import_prompts,
           init_apps,
           add_media_servers,
           allow_sbcs,
           enable_crossbar_mods])
def all(ctx):
    pass
