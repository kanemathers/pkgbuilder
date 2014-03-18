import importlib
import tempfile

import docker

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

        #'FROM base\r\n'
        #'VOLUME ["/repo"]\r\n'
        #'WORKDIR /repo\r\n'
        #'RUN {}\r\n'.format(build_cmd)
        #'RUN {}\r\n'.format(install_cmd)

        #container_id = self.docker.build()

        #self.docker.start(container_id, binds={self.build_dir: '/repo'})
        self.docker.start(container_id, binds={repo.path: '/repo'})

        print container_id
