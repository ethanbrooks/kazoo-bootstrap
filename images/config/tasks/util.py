from os.path import join
import json

from kzconfig.util import (
    quote,
    b64encode,
    b64decode,
    join_url,
    json_dumps,
    addrs_for
)


def load_config(name):
    file_name = name + '.json'
    path = full_path(join('assets', 'config', file_name))
    with open(path) as fd:
        return json.loads(fd.read())


def full_path(rel_path):
    return join('.', rel_path)
