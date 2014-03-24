import os
import subprocess
import shlex
import json

class Repo(object):

    REQUIRED_METAVARS = {
        'package': ('name', 'version'),
        'install': (),
    }

    def __init__(self, path):
        self.path     = path
        self.metadata = None

        self.load_metadata()

    def load_metadata(self, filename='pkgbuild.json'):
        with open(os.path.join(self.path, filename), 'r') as fp:
            self.metadata = json.load(fp)

        for section in self.REQUIRED_METAVARS:
            for key in self.REQUIRED_METAVARS[section]:
                if key not in self.metadata[section]:
                    raise KeyError('{}:{}'.format(section, key))
