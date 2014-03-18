import os
import importlib
import tempfile

import docker
import mako.lookup

here            = os.path.abspath(os.path.dirname(__file__))
template_dir    = os.path.join(here, 'compilers')
template_lookup = mako.lookup.TemplateLookup(directories=[template_dir])

def template(template_name, args):
    t = template_lookup.get_template(template_name)

    return t.render(**args)

class Packager(object):

    def __init__(self):
        self.compilers = set()

    def load_compiler(self, name):
        self.compilers.add(Compiler(name))

    def load_compilers(self, names):
        for name in names:
            self.load_compiler(name)

    def build_package(self, repo):
        for compiler in self.compilers:
            compiler.build_repo(repo)

class Compiler(object):

    def __init__(self, name):
        self.name      = name
        self.build_dir = tempfile.mkdtemp(prefix='pkgbuilder-')
        self.docker    = docker.Client(base_url='unix://var/run/docker.sock',
                                       version='1.6', timeout=10)

    def build_repo(self, repo):
        build_cmd   = repo.metadata['installation'].get('build', 'true')
        install_cmd = repo.metadata['installation']['install']

        dockerfile = template('/arch/dockerfile', {
            'build_cmd':   build_cmd,
            'install_cmd': install_cmd,
        })

        #container_id = self.docker.build()

        #self.docker.start(container_id, binds={self.build_dir: '/repo'})
        #self.docker.start(container_id, binds={repo.path: '/repo'})

        #print container_id
