import tarfile
import tempfile

def init():
    return True

def build_package(packager, repo):
    tarball = archive_repo(repo)

def archive_repo(repo):
    """ Compresses the ``repo`` into a .tar.gz.

    .. note::
       The returned ``File`` object is an instance of
       ``tempfile.NamedTemporaryFile`` and is closed and deleted automatically.
    """

    # Maybe move this into :class:``repos.Repo`` ?

    fp = tempfile.NamedTemporaryFile('w+b', dir='/tmp', delete=True)

    with tarfile.open(fileobj=fp, mode='w:gz') as tar:
        tar.add(repo.path, arcname='')

    return fp
