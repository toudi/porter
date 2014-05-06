from porter.core.module import SIG_SOURCE_POST_SEND
from porter.core.module import SIG_DEPLOY_FINISH
from porter.core.module import SIG_DEPLOY_START
from porter.tools.supervisor import update_supervisor_launcher
from porter.tools.supervisor import stop_group
from porter.tools.supervisor import start_group
from porter.tools.supervisor import reload_cfg


class Plugin(object):
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
                module.get_config_value(
                    'plugins.supervisor',
                    'launcher',
                    '%s.conf' % module.modulename
                )
            ),
            use_sudo=True,
        )

    def finish(self, module):
        reload_cfg(use_sudo=True)
        start_group(module.modulename, use_sudo=True)
