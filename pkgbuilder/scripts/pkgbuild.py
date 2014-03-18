import os
import sys
import argparse

from pkgbuilder.packages import Packager
from pkgbuilder.repos import Repo

# packages for arch linux:
#
# - git clone the remote repo to /tmp/$workingdir/$reponame/src
# - for each package type to build, create the skeletons in
#   /tmp/$workingir/$reponame/pkg/$type/{skeleton}
# - read our metadata file out of /tmp/$workingdir/$reponame/src/pkgbuilder.ini
#     - this gives us package name, version (or read git tag/hash?), authors
#       name, email, url, etc...
# - run the users 'install commands' (from the metadata
#   (./configure && make && make install)) to build and install the code to each
#   /tmp/$workingdir/$reponame/pkg/$type/
# - XXX: somehow create init/systemd scripts for each $type from a common input
#   format
# - run arches makepkg, debians deb-build thingy, etc...
# - serve back the package

def main(args=sys.argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('repo', help='URI for the repo to build packages for')

    args     = parser.parse_args()
    repo     = Repo(args.repo)
    packager = Packager()

    packager.load_package_compilers(('arch', 'opkg'))
    packager.build_package(repo)

    return 0
