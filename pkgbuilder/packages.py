import os
import io
import importlib
import tempfile

import distutils.core
import docker
import mako.template

HERE          = os.path.abspath(os.path.dirname(__file__))
COMPILERS_DIR = os.path.join(HERE, 'compilers')

def template(path, args):
    t = mako.template.Template(filename=path)

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
        self.name       = name
        self.dockerfile = os.path.join(COMPILERS_DIR, self.name, 'dockerfile')
        self.assets     = os.path.join(COMPILERS_DIR, self.name, 'assets')
        self.docker     = docker.Client(base_url='unix://var/run/docker.sock',
                                        version='1.6', timeout=10)

        self.prepare_working_env()

    def build_repo(self, repo):
        # - copy repo into working dir on container
        # - use dockerfile as compiler. setup build env and compile package
        #   into working dir
        # - pkgbuild serves back the packages

        self.prepare_build_env(repo)

        dockerfile = template(self.dockerfile, {
            'install_cmds': repo.metadata['install']
        })

        fp       = io.StringIO(dockerfile) # XXX: close this?
        image_id = self.docker.build(fileobj=fp)[0]

        if not image_id:
            raise Exception('Failed to build image')

        container_id = self.docker.create_container(image_id,
                                                    command='ls /pkgbuild/build',
                                                    volumes=['/pkgbuild'],
                                                    working_dir='/pkgbuild')

        self.docker.start(container_id, binds={self.working_dir: '/pkgbuild'})

        print container_id

    def prepare_working_env(self):
        self.working_dir = tempfile.mkdtemp(prefix='pkgbuilder-')

        self.repo_dir = os.path.join(self.working_dir, 'repo')
        os.makedirs(self.repo_dir)

        self.build_dir = os.path.join(self.working_dir, 'build')
        os.makedirs(self.build_dir)

    def prepare_build_env(self, repo):
        distutils.dir_util.copy_tree(repo.path, self.repo_dir)
        distutils.dir_util.copy_tree(self.assets, self.build_dir)

        for root, dirs, files in os.walk(self.build_dir):
            for file in files:
                if not file.endswith('.tmpl'):
                    continue

                tmpl    = os.path.join(root, file)
                newname = tmpl[:-5]

                with open(newname, 'w') as fp:
                    fp.write(template(tmpl, repo.metadata['package']))

                os.unlink(tmpl)
