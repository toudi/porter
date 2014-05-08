from fabric.api import settings
from fabric.operations import run as frun


def is_link(path):
    with settings(warn_only=True):
        return frun('[ -L "%s" ]' % path).succeeded
