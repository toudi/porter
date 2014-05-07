from porter.core.module import SIG_SOURCE_POST_SEND
from porter.core.module import SIG_DEPLOY_FINISH
from porter.core.module import SIG_DEPLOY_START
from porter.tools.supervisor import update_supervisor_launcher
from porter.tools.supervisor import stop_group
from porter.tools.supervisor import start_group
from porter.tools.supervisor import reload_cfg
from porter.plugins.base import BasePlugin

SIG_LAUNCHER_UPDATED = 'supervisor-launcher-updated'

class Plugin(BasePlugin):
    def command_line_args(self, group):
        group.add_argument('--update-config', '-suc', action='store_true', default=False, help='Update supervisor config files')

    def register_signal_handlers(self, module):
        module.push_signal_handler(SIG_DEPLOY_START, self.start)
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.post_send)
        module.push_signal_handler(SIG_DEPLOY_FINISH, self.finish)

    def start(self, module):
        stop_group(module.modulename, use_sudo=True)

    def post_send(self, module):
        update_supervisor_launcher(
            source_location='%s/supervisor/%s' % (
                module.moduledir,
                self.get_config_value(
                    module,
                    'launcher',
                    '%s.conf' % module.modulename
                )
            ),
            use_sudo=True,
        )
        launcher = '%s/%s.conf' % (self.get_supervisor_path(), module.modulename)
        module.signal(SIG_LAUNCHER_UPDATED, launcher=launcher)

    def get_supervisor_path(self):
        """
        TODO: update this code for locally-installed supervisor
        (i.e. pip install supervisor)
        """
        return '/etc/supervisor/conf.d/'

    def finish(self, module):
        reload_cfg(use_sudo=True)
        start_group(module.modulename, use_sudo=True)
