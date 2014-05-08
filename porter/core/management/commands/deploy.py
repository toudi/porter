from porter.core.management.command import BaseCommand
from porter.core.project import Project
from os import getcwd
from os.path import dirname, basename, exists
from ConfigParser import SafeConfigParser
from importlib import import_module


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.load_config()

    def fill_command_line_args(self, parser, subcommand):
        subcommand.add_argument('--host')
        subcommand.add_argument('--config')
        subcommand.add_argument('--release', '-r', default='stable')
        subcommand.add_argument('--force', default=None, help='Force specific modules to deploy. Specify empty string to force all modules to be re-deployed')

        for plugin in self.config.get('project', 'plugins').split(','):
            plugin_code = import_module(plugin.strip()).Plugin()
            args_group_name = plugin.split('.')[-1]
            group = subcommand.add_argument_group(args_group_name)
            try:
                plugin_code.command_line_args(group)
            except:
                from traceback import print_exc
                print_exc()
                pass

    def handle(self):
        if not self.args['host']:
            print('Please specify a valid host.')
            print('Valid hosts:')
            for name, _ in self.config.items('hosts'):
                print('(*) %s => %s' % (name, _))
            return
        # if not self.args['config']:
        #     print('Please specify a valid config.')
        #     print('Valid configs:')

        project = Project(args=self.args, config=self.config)
        project.deploy()

    def load_config(self):
        cwd = getcwd()
        config_file = 'project.ini'
        if not exists(config_file):
            raise Exception('Config file (%s) not found' % config_file)
        self.logger.debug('Parsing config file [%s]' % config_file)
        config = SafeConfigParser()
        config.read(config_file)
        self.config = config
