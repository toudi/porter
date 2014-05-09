from porter.core.module import SIG_SOURCE_POST_SEND
from porter.core.module import SIG_DEPLOY_FINISH
from porter.tools.scp import scp
from porter.tools.scp import copy_config_file
from porter.plugins.base import BasePlugin
from porter.tools.uwsgi import restart


class Plugin(BasePlugin):

    def command_line_args(self, group):
        group.add_argument('--restart', action='store_true',
                           default=False, help='Restart the uWSGI process')
        group.add_argument('--update-vassal-launcher', action='store_true',
                           default=False, help='Update launcher definition')

    def register_signal_handlers(self, module):
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.post_send)
        module.push_signal_handler(SIG_DEPLOY_FINISH, self.finish)

    def post_send(self, module):
        if bool(self.get_config_value(module, 'emperor')) == True:
            if module.project.args['update-vassal-launcher'] == True:
                for launcher in self.get_config_value(module, 'launcher').split(','):
                    scp(
                        '%s/uwsgi/%s' % (module.moduledir, launcher),
                        self.get_config_value(module, 'vassals_dir')
                    )
                if bool(self.get_config_value(module, 'copy_domains')) == True:
                    copy_config_file(
                        module,
                        'domains.txt',
                    )

    def finish(self, module):
        if module.project.args['restart'] == True:
            for launcher in self.get_config_value(module, 'launcher').split(','):
                restart(
                    '%s/%s' % (
                        self.get_config_value(module, 'pid_dir'),
                        launcher.replace('.ini', '.pid')
                    )
                )
