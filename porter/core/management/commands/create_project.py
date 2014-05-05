from porter.core.management.command import BaseCommand
import os


class Command(BaseCommand):
    def fill_command_line_args(self, parser, subcommand):
        subcommand.add_argument('project-name', help='The projects name')

    def handle(self):
        try:
            os.mkdir(self.args['project-name'])
            self.logger.debug('Creating project dir [%s]' % self.args['project-name'])
        except OSError:
            self.logger.critical('project dir [%s] already exists!' % self.args['project-name'])
