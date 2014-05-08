from porter.plugins.python.base import Plugin as PythonPlugin
from porter.tools.scp import scp
from porter.core.module import SIG_SOURCE_POST_SEND
from porter.tools.virtualenv import virtualenv
from os.path import exists


MANAGE_PY = '%(settings)spython manage.py %(cmd)s'

SIG_SYNCDB = 'django-syncdb'

class Plugin(PythonPlugin):

    def register_signal_handlers(self, module):
        super(PythonPlugin, self).register_signal_handlers(module)
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.copy_settings)

    def copy_settings(self, module):
        settings_file = self.get_config_value(
            module, 'settings_file', None
        )
        subdir = self.get_config_value(module, 'settings_dir')
        if settings_file is not None:
            _settings_file = '%s/%s' % (module.get_config_dir(), settings_file)
            destpath = module.destpath
            if subdir:
                destpath += '/' + subdir
            if exists(_settings_file):
                scp(
                    _settings_file,
                    '%s/%s' % (
                        destpath,
                        settings_file
                    )
                )
        if bool(int(self.get_config_value(module, 'migrate', True))) == True:
            settings = ''
            if settings_file is not None:
                if subdir is not None:
                    settings_file = subdir + '/' + settings_file
                settings_module = settings_file.replace('.py', '').replace('/', '.')
                settings = 'DJANGO_SETTINGS_MODULE=%s ' % settings_module

            manage_cmd = MANAGE_PY % {
                'settings': settings,
                'cmd': 'syncdb --no-initial-data'
            }

            module.signal(SIG_SYNCDB)

            virtualenv(
                module.get_config_value('plugin:porter.plugins.python.virtualenv', 'path'),
                manage_cmd,
                cd_path=module.destpath
            )
            manage_cmd = manage_cmd.replace('syncdb', 'migrate')
            virtualenv(
                module.get_config_value('plugin:porter.plugins.python.virtualenv', 'path'),
                manage_cmd,
                cd_path=module.destpath
            )
