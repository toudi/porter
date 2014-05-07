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
from porter.plugins.base import get_plugin_instance


SIG_SOURCE_PRE_SEND = 0x01
SIG_SOURCE_POST_SEND = 0x02
SIG_SOURCE_SEND = 0x03

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
        self.push_signal_handler(SIG_SOURCE_SEND, self._send_source)

        try:
            deployment = imp.load_source(
                'deployment',
                '%s/deployment.py' %
                self.project.get_module_dir(self.modulename)
            )
            deployment.register_signal_handlers(self)

        except (IOError, AttributeError):
            pass
        # register hooks from plugins
        for plugin in self.plugins():
            plugin.register_signal_handlers(self)

    def depends(self, out=None):
        if out is None:
            out = []

        try:
            config = self.config
            for modulename in config.get('module', 'depends', '').split(','):
                _depends = ProjectModule(modulename, self.project).depends(out)
                # we want to append the dependencies, but without those which
                # have been already processed. we can't use regular set here,
                # because the order is significant
                # original answer:
                # http://stackoverflow.com/questions/1319338/combining-two-lists-and-removing-duplicates-without-removing-duplicates-in-orig
                out += list(set(_depends) - set(out))
        except (NoOptionError, NoSectionError):
            pass

        if self.modulename not in out:
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

    def signal(self, signum, *args, **kwargs):
        try:
            for handler in self.signal_handlers[signum]:
                handler(self, *args, **kwargs)
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

    def _signal_handler_deploy(self, foo):
        self.signal(SIG_DEPLOY_START)
        self.scm.checkout()
        self.signal(SIG_SOURCE_PRE_SEND)
        self.signal(SIG_SOURCE_SEND)
        self.signal(SIG_SOURCE_POST_SEND)
        self.signal(SIG_DEPLOY_FINISH)

    @property
    def destpath(self):
        return self.get_config_value('module', 'path')

    def _send_source(self, module):
        use_rsync = self.get_config_value('module', 'use_rsync', True)
        if use_rsync:
            with lcd('%s/repo' % self.moduledir):
                remote_dir = self.destpath
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
                        "project": self.destpath
                    },
                    rsync_options
                )

    def get_config_dir(self):
        return '%s/config/%s' % (self.moduledir, self.project.args['config'])

    def plugins(self):
        for section in self.config.sections():
            if section.startswith('plugin:'):
                yield get_plugin_instance(section.replace('plugin:', ''))

    @property
    def version(self):
        try:
            return self.scm.version
        except NoSectionError:
            return self.get_config_value(
                'release:%s' % self.project.args['release'], 'version'
            )
