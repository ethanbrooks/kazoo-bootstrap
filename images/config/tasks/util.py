from os.path import join
import json

from . import BASE_PATH


def load_config(name):
    file_name = name + '.json'
    path = full_path(join('assets', 'config', file_name))
    with open(path) as fd:
        return json.loads(fd.read())


def full_path(rel_path):
    return join(BASE_PATH, rel_path)
