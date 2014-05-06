from porter.core.module import SIG_SOURCE_POST_SEND
from porter.plugins.base import BasePlugin
from porter.tools.sed import sed_replace
from fabric.contrib.files import exists as rexists
from porter.tools.virtualenv import setup_virtualenv
from porter.tools.virtualenv import virtualenv


class Plugin(BasePlugin):

    def register_signal_handlers(self, module):
        super(Plugin, self).register_signal_handlers(module)
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.post_send)

    def post_send(self, module):
        venv_path = module.get_config_value('plugins.virtualenv', 'path')
        setup_virtualenv(venv_path)
        requirements_file = module.get_config_value('plugins.virtualenv', 'requirements')
        if requirements_file is not None:
            requirements_file = requirements_file.replace('__destpath__', module.destpath)
            virtualenv(
                venv_path,
                'pip install -r %s' % requirements_file
            )

        files = module.get_config_value(
            'plugins.virtualenv', 'update_files', '').split(',')
        for _file in files:
            if rexists(_file):
                sed_replace(
                    {
                        'env': module.get_config_value('plugins.virtualenv', 'path'),
                        'project': module.destpath
                    },
                    _file,
                    use_sudo=True
                )
