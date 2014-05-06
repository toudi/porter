from porter.plugins.python.base import Plugin as PythonPlugin
from porter.tools.scp import scp
from porter.core.module import SIG_SOURCE_POST_SEND
from porter.tools.virtualenv import virtualenv


class Plugin(PythonPlugin):

    def register_signal_handlers(self, module):
        super(PythonPlugin, self).register_signal_handlers(module)
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.copy_settings)

    def copy_settings(self, module):
        scp(
            '%s/%s' % (
                module.get_config_dir(),
                module.get_config_value('plugins.django', 'settings_file')
            ),
            '%s/%s' % (
                module.destpath,
                module.get_config_value('plugins.django', 'settings_file')
            )
        )
        settings_file = module.get_config_value('plugins.django', 'settings_file', 'settings.py').replace('.py', '').replace('/','.')

        virtualenv(
            module.get_config_value('plugins.virtualenv', 'path'),
            'DJANGO_SETTINGS_MODULE=%s python manage.py syncdb --no-initial-data' % settings_file,
            cd_path=module.destpath
        )
        virtualenv(
            module.get_config_value('plugins.virtualenv', 'path'),
            'DJANGO_SETTINGS_MODULE=%s python manage.py migrate --no-initial-data' % settings_file,
            cd_path=module.destpath
        )
