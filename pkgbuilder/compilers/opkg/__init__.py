def init():
    return True

def build_package(packager, repo):
    print 'building {}'.format(repo.metadata['package']['name'])
