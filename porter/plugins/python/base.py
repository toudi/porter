from porter.core.module import SIG_SOURCE_POST_SEND
from porter.plugins.base import BasePlugin
from porter.tools.python import remove_pyc_files


class Plugin(BasePlugin):

    def register_signal_handlers(self, module):
        super(Plugin, self).register_signal_handlers(module)
        module.push_signal_handler(SIG_SOURCE_POST_SEND, self.source_post_send)

    def source_post_send(self, module):
        remove_pyc_files(module.destpath)
