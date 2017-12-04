# from invoke import task
# from kzconfig import kube, dns
#
# from . import util
#
#
# @task(default=True)
# def add_cnames(ctx):
#     print('Adding cnames ...')
#     for names, target in ctx.dns['cnames']:
#         for name in names:
#             print(dns.add('CNAME', name, target, domain=ctx.dns['domain']))


# cnames: kube, drone, s3
#
# api, my -> cluster.valuphone.com
# cnames: ws, wss -> sip.valuphone.com -> saturn.valuphone.com

# cnames: kube, drone, s3, api, my ->
# sip-proxy -> tag:sip-proxy
# media-server -> tag:media-server
#
# ws, wss -> sip-proxy.
