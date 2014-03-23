import os
import io
import importlib
import tempfile

import distutils.core
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
        self.name   = name
        self.assets = os.path.join(here, 'compilers', self.name, 'assets')
        self.docker = docker.Client(base_url='unix://var/run/docker.sock',
                                    version='1.6', timeout=10)

        self.prepare_working_env()

    def build_repo(self, repo):
        # - copy repo into working dir on container
        # - use dockerfile as compiler. setup build env and compile package
        #   into working dir
        # - pkgbuild serves back the packages

        self.prepare_build_env(repo)

        build_cmd   = repo.metadata['installation'].get('build', 'true')
        install_cmd = repo.metadata['installation']['install']

        dockerfile = template('/{0}/dockerfile'.format(self.name), {
            'build_cmd':   build_cmd,
            'install_cmd': install_cmd,
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
