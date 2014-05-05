class Plugin(object):
    def command_line_args(self, group):
        group.add_argument('--restart', action='store_true', default=False, help='Restart the uWSGI process')
