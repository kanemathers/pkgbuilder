import importlib
import tempfile

class Packager(object):

    def __init__(self):
        self.working_dir = tempfile.mkdtemp(dir='/tmp', prefix='pkgbuilder-pkg')
        self.compilers   = set()

    def load_compiler(self, name):
        self.compilers.add(Compiler(name))

    def load_compilers(self, names):
        for name in names:
            self.load_compiler(name)

    def build_package(self, repo):
        for compiler in self.compilers:
            compiler.module.build_package(self, repo)

class Compiler(object):

    def __init__(self, name):
        self.name = name

        try:
            self.module = self._load_module(self.name)

            self.module.init()
        except (ImportError, AttributeError):
            raise ImportError('failed to initialize compiler: {}'.format(name))

    def _load_module(self, name):
        module = 'pkgbuilder.compilers.{}'.format(name)

        return importlib.import_module(module, 'pkgbuilder')
