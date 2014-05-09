from porter.core.module import SIG_SOURCE_POST_SEND
from porter.plugins.base import BasePlugin
from porter.tools.sed import sed_replace
from fabric.contrib.files import exists as rexists
from porter.tools.virtualenv import setup_virtualenv
from porter.tools.virtualenv import virtualenv
from porter.plugins.supervisor import SIG_LAUNCHER_UPDATED


class Plugin(BasePlugin):

    def command_line_args(self, group):
        group.add_argument('--update-requirements', action='store_true',
                           default=False,
                           help='Install or update requirements to virtualenv')

    def register_signal_handlers(self, module):
        super(Plugin, self).register_signal_handlers(module)
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.post_send)
        module.push_signal_handler(SIG_LAUNCHER_UPDATED, self.replace_path)

    def post_send(self, module):
        venv_path = self.get_config_value(module, 'path')
        setup_virtualenv(venv_path)
        if module.project.args['update-requirements'] is True:
            requirements = self.get_config_value(module, 'requirements')
            if requirements is not None:
                requirements = requirements.split(',')
                for requir in requirements:
                    if requir.startswith('file:'):
                        requir = requir.replace('__destpath__', module.destpath)
                        _what = '-r %s' % requir
                    else:
                        _what = '"%s"' % requir

                    virtualenv(
                        venv_path,
                        'pip install %s' % _what
                    )

    def replace_path(self, module, launcher, use_sudo):
        if rexists(launcher):
            sed_replace(
                {
                    'env': self.get_config_value(module, 'path'),
                    'project': module.destpath
                },
                launcher,
                use_sudo=use_sudo
            )
