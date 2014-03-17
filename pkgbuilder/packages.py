import importlib
import collections
import shutil
import tempfile
import subprocess
import shlex
import json

class Compiler(object):

    def __init__(self, name):
        self.name = name

        try:
            self.module = self.load_module(self.name)

            self.module.init()
        except (ImportError, AttributeError):
            raise ImportError('failed to initialize module: {}'.format(name))

    def load_module(self, name):
        module = 'pkgbuilder.compilers.{}'.format(name)

        return importlib.import_module(module, 'pkgbuilder')

    def load_modules(self, modules):
        for name in modules:
            self.load_module(name)

class Packager(object):

    def __init__(self):
        self.working_dir = tempfile.mkdtemp(dir='/tmp', prefix='pkgbuilder-pkg')
        self.compilers   = set()

    def load_package_compiler(self, type):
        self.compilers.add(Compiler(type))

    def load_package_compilers(self, package_types):
        for type in package_types:
            self.load_package_compiler(type)

    def build_package(self, repo):
        for compiler in self.compilers:
            compiler.module.build_package(self, repo)
