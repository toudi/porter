Module
======

Module is an atomic part of your project. One module can depend on other modules

A module can use plugins, which extend the available command-line arguments
when doing a deploy command.

Plugins
-------
If you want to use some of the plugins, just add it's corresponding section
to the ini file which starts with 'plugin:', like so: ::

    (mymodule.ini)
    [plugin:porter.plugins. ... ]

the verbose naming convention is no accident. If you want to use some plugin
which isn't located inside porter's codebase, then you simply append it to
your PYTHONPATH and thanks to the naming convention, porter can import the
code: ::

    (mymodule.ini)
    [plugin:my.private.plugin]

During the deployment procedure, several signals are launched. Each of the plugins
can listen to these signals and do something about it.

Available signals:

===================== =======================================================
Signal code           Sent on
===================== =======================================================
SIG_SOURCE_PRE_SEND   Before the source is rsynced to the destination machine
SIG_SOURCE_POST_SEND  After the source is rsynced
SIG_SOURCE_SEND       This signal is used to perform the actual source code
                      deployment. If you want to overwrite it by your own
                      callable, use deployment.py file
SIG_DEPLOY_START      Entry point for the module's deployment procedure
SIG_DEPLOY_FINISH     Exit point for the module's deployment procedure
SIG_DEPLOY            This signal is sent to perform the actual deployment.
                      If you want to overwrite it, use deployment.py
===================== =======================================================

deployment.py
-------------

Let's be honest - there is no such thing as an ideal config. IT projects are
complex beasts and sometimes you want to add personal flavor to it. Here's
where deployment.py kicks in. You can use this file in order to add additional
handlers to the signals, or to replace then altogether.

You need to place this file inside the module's directory.

Example file::

    from porter.core.module import SIG_SOURCE_POST_SEND
    def register_signal_handlers(module):
        module.push_signal_handler(SIG_SOURCE_POST_SEND, post_send)

    def post_send(module, *args, **kwargs):
        pass

Configuration
-------------

When you're deploying, it's safe to say that you have different configurations
depending on the machine you're using (i.e. you use different database 
configurations on testing and production machine, etc). Porter must know where
to fetch such files. This is why you can create config subdirectories
within your module: ::

    mymodule/
    mymodule/config/
    mymodule/config/production/
    mymodule/config/production/local_settings.py
    mymodule/config/testing/
    mymodule/config/testing/local_settings.py

You can then specify this config by the `config` parameter: ::

    porter-admin deploy --config testing

if you are adding your own deployment hooks, porter offers you an API for
copying such files: ::

    from porter.tools.scp import copy_config_file

    copy_config_file(module, 'local_settings.py')

which would copy local_settings.py from appropriate location
