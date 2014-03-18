import importlib

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
        self.name   = name
        self.docker = docker.Client(base_url='unix://var/run/docker.sock',
                                    version='1.6', timeout=10)

    def build_repo(self, repo):
        container_id = self.docker.create_container('base', 'ls /tmp/repo',
                                                    volumes=['/tmp/repo'])

        self.docker.start(container_id, binds={repo.path: '/tmp/repo'})

        print container_id
