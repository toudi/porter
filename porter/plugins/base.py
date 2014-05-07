from importlib import import_module


class BasePlugin(object):

    def register_signal_handlers(self, module):
        pass

    def get_config_value(self, module, option, default=None):
        return module.get_config_value(
            'plugin:%s' % self.__module__, option, default
        )


def get_plugin_instance(name):
    return import_module(name).Plugin()
