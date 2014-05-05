from os.path import dirname
from os.path import basename
from fabric.contrib.files import exists as rexists
from fabric.context_managers import cd
from fabric.api import run
from fabric.api import sudo


def setup_virtualenv(path):
    if not rexists(path):
        run('mkdir -p %s' % dirname(path))
        with cd(dirname(path)):
            run('virtualenv %s' % basename(path))


def virtualenv(ve_path, command, use_sudo=False, cd_path=None):
    def do_virtualenv(ve_path, command, use_sudo=False):
        command = '. %(path)s/bin/activate && %(command)s' % {
            'path': ve_path,
            'command': command
        }

        if use_sudo:
            sudo(command, shell=False)
        else:
            run(command)

    if cd_path:
        with cd(cd_path):
            do_virtualenv(ve_path, command, use_sudo)
    else:
        do_virtualenv(ve_path, command, use_sudo)
