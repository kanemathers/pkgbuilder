import os
import sys
import argparse

from pkgbuilder.packages import Packager
from pkgbuilder.repos import Repo

def main(args=sys.argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('repo', help='URI for the repo to build packages for')

    args     = parser.parse_args()
    repo     = Repo(args.repo)
    packager = Packager()

    packager.load_compilers(('deb',))
    packager.build_package(repo)

    return 0
