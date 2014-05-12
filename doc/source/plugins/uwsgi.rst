uWSGI
=====

Use this plugin if you're hosting your application using uWSGI application server.

Available command-line arguments:

\-\-restart
    Restart uwsgi process after the deployment. By default, this switch is turned
    off.

\-\-update-vassal-launcher
    To be used with emperor mode. If something changed in your vassal launcher
    file and it needs to be updated, use this switch.

Available variables inside the module ini file:

emperor
    Use uwsgi emperor mode. currently, the only supported mode :/
launcher
    CSV line of launcher files (uwsgi vassals). The files need to be placed
    inside 'uwsgi' subdirectory of module directory.
vassals_dir
    Directory for storing the vassals
pid_dir
    Directory for storing the pids of master processes. This is needed for
    application restarting, using kill -HUP `cat pidfile`
