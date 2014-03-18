import os

from setuptools import (
    setup,
    find_packages,
)

from pkgbuilder import (
    __VERSION__,
    __AUTHOR__,
    __AUTHOR_EMAIL__,
)

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, 'readme.md'), 'r') as fp:
        readme = fp.read()
except IOError:
    readme = ''

try:
    with open(os.path.join(here, 'changes.md'), 'r') as fp:
        changes = fp.read()
except IOError:
    changes = ''

requires = [
    'docker-py',
    'mako',
]

setup(name='pkgbuilder',
      version=__VERSION__,
      description='',
      long_description='{0}\r\n{1}'.format(readme, changes),
      author=__AUTHOR__,
      author_email=__AUTHOR_EMAIL__,
      url='https://github.com/kanemathers/pkgbuilder',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      pkgbuild = pkgbuilder.scripts.pkgbuild:main
      """)
