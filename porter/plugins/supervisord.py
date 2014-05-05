class Plugin(object):
    def command_line_args(self, group):
        group.add_argument('--update-config', '-suc', action='store_true', default=False, help='Update supervisor config files')
