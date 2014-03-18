import os
import sys
import argparse

from pkgbuilder.packages import Packager
from pkgbuilder.repos import Repo

# - repo can be a path to a local directory, url to archive, git remote, etc.
# - repo is downloaded to host
# - pkgbuild.json is read out of repo
#   - gives us package name, version, authors name and email, url, etc...
#   - package dependencies?
# - for each compiler loaded (arch, debian, opkg, etc) fire up a docker
#   container with the native OS
# - prepare package skeleton inside container (arch needs a PKGBUILD, debs
#   need their folder structure and shit setup, etc...)
# - build repo inside container/skeleton (pkgbuild.json's ``installation:build``
#   and ``installation:install`` commands)
# - run the OSs package builder tool (arch's makepkg, debians deb-build thingy,
#   etc)
# - serve back the compiled packages to the user

# will also need:
# - some way to create init.d/systemd scripts from a common input format
# - pre/post install hooks for the packages from a common input format

def main(args=sys.argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('repo', help='URI for the repo to build packages for')

    args     = parser.parse_args()
    repo     = Repo(args.repo)
    packager = Packager()

    packager.load_compilers(('arch', 'opkg'))
    packager.build_package(repo)

    return 0
