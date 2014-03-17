import os
import tempfile
import json
import subprocess
import shlex
import hashlib

class Repo(object):

    REQUIRED_METAVARS = {
        'package': ('name', 'version')
    }

    def __init__(self, path):
        self.path     = path
        self.metadata = None

        self.load_metadata()

    def load_metadata(self, filename='pkgbuilder.json'):
        with open(os.path.join(self.path, filename), 'r') as fp:
            self.metadata = json.load(fp)

        for section in self.REQUIRED_METAVARS:
            for key in self.REQUIRED_METAVARS[section]:
                if key not in self.metadata[section]:
                    raise KeyError('{}:{}'.format(section, key))

def build(repo):
    """ Extracts the ``installation:build`` commands from the ``repo``s
    metadata and executes them on the host.
    """

    try:
        cmd = repo.metadata['installation']['build']
    except KeyError:
        return

    p = subprocess.Popen(shlex.split(cmd))

    return p.wait()

def install(repo):
    """ Extracts the ``installation:install`` commands from the ``repo``s
    metadata and executes them on the host.
    """

    try:
        cmd = repo.metadata['installation']['install']
    except KeyError:
        return

    p = subprocess.Popen(shlex.split(cmd))

    return p.wait()
