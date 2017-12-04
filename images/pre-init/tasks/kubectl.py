# import os.path
#
#
# from invoke import task
# from kzconfig import Context
# from kzconfig.util import read_config
#
# context = Context()
#
# @task
# def config(ctx):
#     kubectl = context.kubectl
#     if os.path.exists(ctx.kubectl['base_path']):
#         print('Bootstrapping kube-config ...')
#         token = read_config('token', base=ctx.kubectl['base_path'])
#         namespace = read_config('namespace', base=ctx.kubectl['base_path'])
#
#         ctx.run(kubectl.config.set_credentials(
#             ctx.kubectl['user'], token=token
#         ))
#         ctx.run(kubectl.config.set_context(
#             ctx.kubectl['context'], ctx.kubectl['cluster'],
#             ctx.kubectl['user'], namespace=namespace
#         ))
