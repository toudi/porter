from porter.core.module import SIG_SOURCE_POST_SEND
from porter.core.module import SIG_DEPLOY_FINISH
from porter.tools.scp import scp
from porter.plugins.base import BasePlugin
from fabric.operations import run


class Plugin(BasePlugin):
    def command_line_args(self, group):
        group.add_argument('--restart', action='store_true', default=False, help='Restart the uWSGI process')

    def register_signal_handlers(self, module):
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.post_send)
        module.push_signal_handler(SIG_DEPLOY_FINISH, self.finish)

    def post_send(self, module):
        self.file = self.get_config_value(module, 'file', module.modulename)
        if not self.file.endswith('.crontab'):
            self.file += '.crontab'

        scp(
            '%s/crontab/%s' % (
                module.moduledir,
                self.file
            ),
            '/tmp'
        )

    def finish(self, module):
        run('crontab /tmp/%s && rm -f /tmp/%s' % (self.file, self.file))
