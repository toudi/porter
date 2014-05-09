from porter.core.module import SIG_SOURCE_POST_SEND
from porter.core.module import SIG_DEPLOY_FINISH
from porter.tools.scp import scp
from porter.plugins.base import BasePlugin
from fabric.operations import run


class Plugin(BasePlugin):
    def command_line_args(self, group):
        group.add_argument('--update-crontab', action='store_true', default=False, help='Update crontab')

    def register_signal_handlers(self, module):
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.post_send)
        module.push_signal_handler(SIG_DEPLOY_FINISH, self.finish)

    def get_crontab_file(self, module):
        _file = self.get_config_value(module, 'file', module.modulename)
        if not _file.endswith('.crontab'):
            _file += '.crontab'
        return _file

    def post_send(self, module):
        _file = self.get_crontab_file(module)
        scp(
            '%s/crontab/%s' % (
                module.moduledir,
                _file
            ),
            '/tmp'
        )

    def finish(self, module):
        if module.project.args['update-crontab'] is True:
            _file = self.get_crontab_file(module)
            run('crontab /tmp/%s && rm -f /tmp/%s' % (_file, _file))
