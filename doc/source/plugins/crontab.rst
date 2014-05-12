Crontab
=======

This plugin is used to update crontab entries

Available command-line arguments:

\-\-update-crontab
    If you use this switch, the plugin will look for crontab file, send it
    to destination machine and update crontab entries.

Available variables inside the module ini file:

file [optional, default: module name.crontab]
    The file to look for. It should be placed in 'crontab' subdirectory of your
    module.
