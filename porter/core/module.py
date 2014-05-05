from os.path import basename
from ConfigParser import SafeConfigParser
from ConfigParser import NoOptionError
from ConfigParser import NoSectionError
import imp
from porter.core.scm.loader import get_scm_instance
from fabric.context_managers import lcd
from fabric.api import env
from porter.tools.rsync import rsync
from fabric.contrib.files import exists as rexists
from fabric.operations import run


SIG_SOURCE_PRE_SEND = 0x01
SIG_SOURCE_POST_SEND = 0x02
SIG_SOURCE_DEPLOYMENT_INIT = 0x10
SIG_SOURCE_DEPLOYMENT_FINISH = 0x11
SIG_DEPLOY_START = 0x20
SIG_DEPLOY_FINISH = 0x21
SIG_DEPLOY = 0x30


class ProjectModule(object):
    def __init__(self, modulename, project):
        self.modulename = modulename
        self.project = project
        self.moduledir = project.get_module_dir(modulename)
        self.signal_handlers = {}
        self.push_signal_handler(SIG_DEPLOY, self._signal_handler_deploy)
        self.push_signal_handler(SIG_SOURCE_PRE_SEND, self._signal_handler_source_pre_send)
        try:
            deployment = imp.load_source(
                'deployment',
                '%s/deployment.py' %
                self.project.get_module_dir(self.modulename)
            )
            self.replace_signal_handler(
                SIG_DEPLOY,
                getattr(deployment, 'deploy', self._signal_handler_deploy)
            )
            self.replace_signal_handler(
                SIG_SOURCE_PRE_SEND,
                getattr(
                    deployment,
                    'source_pre_send',
                    self._signal_handler_source_pre_send
                )
            )
        except IOError:
            pass


    def depends(self):
        out = []
        try:
            config = self.config
            for modulename in config.get('module', 'depends', '').split(','):
                out.extend(ProjectModule(modulename, self.project).depends())

        except (NoOptionError, NoSectionError):
            pass
        out.append(self.modulename)
        return out

    @property
    def config(self):
        module_config_file = "%s/%s.ini" % (
            self.moduledir,
            basename(self.moduledir)
        )
        config = SafeConfigParser()
        config.read(module_config_file)
        return config

    def deploy(self):
        self.signal(SIG_DEPLOY)

    def signal(self, signum):
        try:
            for handler in self.signal_handlers[signum]:
                handler(self)
        except KeyError:
            pass

    @property
    def scm(self):
        scm = get_scm_instance(self.config.get('scm', 'url'), self)
        release = dict(self.config.items(
            'release:%s' % self.project.args['release']
        ))
        scm.set_version(**release)
        return scm

    def get_config_value(self, section, option, default=None):
        try:
            return self.config.get(
                section, '%s-%s' % (option, self.project.args['host'])
            )
        except NoSectionError:
            return default
        except NoOptionError:
            try:
                return self.config.get(section, option)
            except:
                return default
        except:
            return default

    def push_signal_handler(self, signal, handler):
        if signal not in self.signal_handlers:
            self.signal_handlers[signal] = []
        self.signal_handlers[signal].append(handler)

    def pop_signal_handler(self, signal):
        self.signal_handlers[signal].pop()

    def replace_signal_handler(self, signal, handler):
        self.pop_signal_handler(signal)
        self.push_signal_handler(signal, handler)

    def _signal_handler_source_pre_send(self, foo):
        pass

    def _signal_handler_deploy(self, foo):
        self.signal(SIG_DEPLOY_START)
        self.scm.checkout()
        self.signal(SIG_SOURCE_PRE_SEND)
        self.send_source()
        self.signal(SIG_SOURCE_POST_SEND)
        self.signal(SIG_DEPLOY_FINISH)

    def send_source(self):
        use_rsync = self.get_config_value('module', 'use_rsync', True)
        if use_rsync:
            with lcd('%s/repo' % self.moduledir):
                remote_dir = self.get_config_value('module', 'path')
                if not rexists(remote_dir):
                    run('mkdir -p %s' % remote_dir)

                rsync_options = {
                    '--progress': True,
                    '--exclude': '.git*',
                }
                rsync(
                    "./",
                    "%(user)s@%(host)s:%(project)s" % {
                        "user": env.user,
                        "host": env.host,
                        "project": self.get_config_value('module', 'path')
                    },
                    rsync_options
                )
