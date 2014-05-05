from os.path import exists
from fabric.operations import local, run
from fabric.context_managers import lcd


class SCM(object):
    def __init__(self, url, module):
        self.url = url
        self.module = module
        self._workdir = '%s/repo' % module.moduledir
        self.version = 'master'

    def set_version(self, tag=None, branch=None):
        if tag:
            self.version = tag
        elif branch:
            self.version = branch

    def checkout(self):
        with lcd(self.module.moduledir):
            if not exists(self._workdir):
                local('git clone %s repo' % self.url)
        with lcd('%s/repo' % self.module.moduledir):
            local('git pull')
            local('git checkout %s' % self.version)
