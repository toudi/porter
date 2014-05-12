Available plugins
=================

During the deployment procedure, several hooks are signalled to the modules.

A plugin is a piece of code, which can do something with your module on those 
hooks. For instance, if your module has to have some crontab entries, porter 
has a plugin which hooks into the `FINISH` signal and does just that. 
If your module is a python-based web application which needs to have a 
virtualenv - porter has a plugin which can do it for you.

Each plugin can extend the available command-line arguments. Here's an example
of how my own project's command-line looks like:::

    porter-admin.py deploy --help
    usage: porter-admin.py deploy [-h] [--host HOST] [--config CONFIG]
                                  [--release RELEASE] [--force FORCE]
                                  [--update-crontab] [--update-requirements]
                                  [--update-launcher] [--restart]
                                  [--update-vassal-launcher] [--migrate-database]

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST
      --config CONFIG
      --release RELEASE, -r RELEASE
      --force FORCE         Force specific modules to deploy. Specify empty string
                            to force all modules to be re-deployed

    porter.plugins.crontab:
      --update-crontab      Update crontab

    porter.plugins.python.virtualenv:
      --update-requirements
                            Install or update requirements to virtualenv

    porter.plugins.supervisor:
      --update-launcher     Update supervisor launcher

    porter.plugins.uwsgi:
      --restart             Restart the uWSGI process
      --update-vassal-launcher
                            Update launcher definition

    porter.plugins.python.django:
      --migrate-database    Perform database migrations

Contents:

.. toctree::
   :maxdepth: 2

   ./python/base
   ./python/virtualenv
   ./python/django
   ./crontab
   ./supervisor
   ./uwsgi
