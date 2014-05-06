from fabric.operations import run
from fabric.context_managers import cd


def remove_pyc_files(path):
    with cd(path):
        run("find . -name '*.pyc' -delete")
