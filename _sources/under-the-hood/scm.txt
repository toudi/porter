Source control management
=========================

SCM classes are used to fetch current revision of your source code from repository
and deploy it to target host.

Currently, there two scm's are implemented:

git
    GIT support
none
    This is not really a scm controller, and it should probably be removed
    in the future. It's used for a scenario, where you want to install
    a package from PyPi into the virtualenv, but use a fixed version instead
    of current one.

Based on which scm you use, there are different attributes you can specify to
check specific version of the code. For example: ::

    [scm]
    url = git://git@myurl.tld/repo.git

    [release:stable]
    branch = master

    [release:unstable]
    tag = never-deploy-that
