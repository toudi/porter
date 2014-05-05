import logging
from fabric.api import env
from fabric.api import run
from fabric.network import disconnect_all
from porter.core.module import ProjectModule
import os.path
from os.path import dirname
from os import getcwd
from ConfigParser import NoOptionError, NoSectionError



class Project(object):
    def __init__(self, args, config):
        self.config = config
        self.config.read('project.ini')
        self.args = args
        self.logger = logging.getLogger(__name__)

    def modules(self):
        pass

    def deploy(self):
        env.host_string = self.config.get('hosts', self.args['host'])
        if '@' in env.host_string:
            env.user, env.host = env.host_string.split('@')
        env.forward_agent = True
        self.logger.debug(
            'Starting deployment of %s' % self.config.get('project', 'name')
        )
        for module in self.depends():
            self.logger.debug('Deploying module %s' % module)
            self.get_module(module).deploy()
            # print(module)
        # run('uname -s')
        disconnect_all()

    def depends(self):
        out = []
        for modulename in self.config.get('project', 'depends').split(','):
            m = self.get_module(modulename)
            out.extend(m.depends())
        return out

    def get_module_dir(self, module):
        try:
            module_dir = self.config.get('modules', module)
        except NoOptionError, NoSectionError:
            module_dir = module

        return os.path.sep.join((getcwd(), module_dir))

    def get_module(self, module):
        return ProjectModule(module, self)
