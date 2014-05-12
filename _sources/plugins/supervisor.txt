Supervisor plugin
=================

If you want to launch some daemons using supervisor, use this plugin.

The plugin will stop your launcher before source code deployment, and re-launch
it after the deployment is done (and code is updated).

Available command-line arguments:

\-\-update-launcher
    If you want to update supervisor's definition of your launcher, use
    this switch. 

Available variables inside the module ini file:

launcher [optional, default: module name.conf]
    During the deployment process, the plugin will copy launcher file from within
    your module's 'supervisor' directory into the destpath

After the launcher is copied to the destination machine, the plugin launches
a signal (SIG_LAUNCHER_UPDATED) with the launcher path. You can hook up to this
signal and react to it. By default, the virtualenv plugin listens to the
signal and updates the paths accordingly
