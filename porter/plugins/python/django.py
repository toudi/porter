from porter.plugins.python.base import Plugin as PythonPlugin
from porter.tools.scp import scp
from porter.core.module import SIG_SOURCE_POST_SEND
from porter.tools.virtualenv import virtualenv
from os.path import exists


class Plugin(PythonPlugin):

    def register_signal_handlers(self, module):
        super(PythonPlugin, self).register_signal_handlers(module)
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.copy_settings)

    def copy_settings(self, module):
        settings_file = self.get_config_value(module, 'settings_file', 'settings.py')
        if exists(settings_file):
            scp(
                '%s/%s' % (
                    module.get_config_dir(),
                    settings_file
                ),
                '%s/%s' % (
                    module.destpath,
                    settings_file
                )
            )
        settings_module = settings_file.replace('.py', '').replace('/', '.')

        virtualenv(
            module.get_config_value('plugin:porter.plugins.python.virtualenv', 'path'),
            'DJANGO_SETTINGS_MODULE=%s python manage.py syncdb --no-initial-data' % settings_module,
            cd_path=module.destpath
        )
        virtualenv(
            module.get_config_value('plugin:porter.plugins.python.virtualenv', 'path'),
            'DJANGO_SETTINGS_MODULE=%s python manage.py migrate --no-initial-data' % settings_module,
            cd_path=module.destpath
        )
