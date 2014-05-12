Django plugin
=============

This plugin helps you with deploying your django-based apps

Available command-line arguments:

--migrate-database
    After source is deployed, you can use this switch to perform database
    migrations (syncdb and / or south's migrate). This switch is optional.

Available variables inside the module ini file:

migrate [optional]:
    If you want to explicitely disable the database migrations for this module,
    set this to 0. Other modules won't be affected
settings_file [optional, default: local_settings.py]
    If you have `settings_file` within your config/[config] directory, it
    will be copied to your project's destpath.

    This is useful, if your settings.py looks like this: ::

        (...)
        from local_settings import *

settings_dir  [optional]
    If your local_settings should be located in some subdirectory of the
    project's root directory, specify it here.

Example sections::

    [plugin:porter.plugins.python.django]
    ; this is an empty section, therefore the plugin will try to look for
    ; local_settings.py inside the config subdirs and it will copy it
    ; to project destpath

    [plugin:porter.plugins.python.django]
    ; disable all migrations on this module, even if --migrate-database is
    ; specified
    migrate = 0

    [plugin:porter.plugins.python.django]
    ; copy myconfig.py instead of local_settings.py
    settings_file = myconfig.py
    ; place it within project/settings/config dir
    settings_dir  = settings/config
