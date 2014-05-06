from importlib import import_module


class BasePlugin(object):

    def register_signal_handlers(self, module):
        pass


def get_plugin_instance(name):
    return import_module(name).Plugin()
