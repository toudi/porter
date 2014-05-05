import argparse
import porter.core.management.commands
import os.path
from importlib import import_module
from copy import deepcopy
import logging


def get_commands():
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    try:
        return [f[:-3] for f in os.listdir(commands_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []

def import_command(command):
    return import_module('porter.core.management.commands.%s' % command).Command

def execute_from_commandline():
    parser = argparse.ArgumentParser(description='Porter management commands')
    parser.add_argument('--verbose', action='store_true')
    commands = parser.add_subparsers(title='subcommands', description='Available subcommands')
    callables = {}
    for cmd in get_commands():
        subcommand = commands.add_parser(cmd)
        _cmd = import_command(cmd)([])
        _cmd.fill_command_line_args(parser, subcommand)
        subcommand.set_defaults(cmd=cmd)

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('paramiko.transport').setLevel(logging.CRITICAL)
    if args.cmd:
        _args = deepcopy(args.__dict__)
        _args.pop('cmd')
        selected_command = import_command(args.cmd)(_args)
        selected_command.handle()
