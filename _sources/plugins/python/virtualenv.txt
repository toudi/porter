Virtualenv plugin
=================

This plugin keeps track of your virtualenv for the modules.

Available command-line arguments:

--update-requirements
    if you specify requirement locations in the ini file, this plugin can
    install the requirements before source code is deployed to the machine,
    so that no import errors occur. This option is switched off by default,
    because this can be a lengthy process, and is not needed every time you
    do a deployment

Available variables inside the module ini file:

path
    A path within server where the virtualenv should be created.
    Missing parent directories will be created automatically (using mkdir -p)
requirements
    If your module has some requirements which need to be installed into
    the newly created virtualenv, you can specify them here.

    multiple requirements must be joined by comma. If you want to install
    requirements from text file, you must prefix it with `file:`. If you want to
    refer to the module destination path, you must prefix it with `__destpath__`

Example section::

    [plugin:porter.plugins.python.virtualenv]
    path = /home/path/module-venv
    requirements = gevent,file:__destpath__/requirements/common.txt,file:__destpath__/requirements/production.txt

Please note, that virtualenv plugin can be linked to be used together with
supervisor plugin. For the details, please refer to the supervisor plugin
documentation
