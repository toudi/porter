Quickstart
==========

In this tutorial we're going to take a quick look on porter and what it can
do for you in order to make your life easier when it comes to deploying your
code.


Create a project directory
~~~~~~~~~~~~~~~~~~~~~~~~~~

Porter assumes, that your project consists of modules, which can be dependent
on each other. each project must have it's own directory.::

    mkdir project
    cd project
    touch project.ini

project.ini
~~~~~~~~~~~

In this file, we are going to specify what is the root module of your project::

    [project]
    name = My great project
    depends = root

    [hosts]
    testing = user@testing-host.tld
    production = user@production-host.tld
    vbox = user@192.168.56.101

You can specify a different directory for your modules, if you don't want to
make a mess out of your project directory, by adding a section `modules` to
the project.ini file, like so::

    [modules]
    module1 = workers/module1

Adding modules
~~~~~~~~~~~~~~
This is where the fun begins!

In order to deploy a module, porter must know something about it. Let's create
a module directory, and see what we can put inside module definition file.::

    mkdir root
    touch root/root.ini

Please note, that the .ini file must be named the same way as the module itself.

Example .ini file:::

    [module]
    path = /home/user/project/apps/root
    path-vbox = /different/path/on/vbox
    depends = uwsgi,module1

    [scm]
    url = git://git@myrepo.tld:reponame.git

    [release:stable]
    branch = release/0.1.2

Let's examine this file and see what does it mean.

`module` section:

**path**
    This is a special variable, which will specify where the source code has
    to be uploaded to.
**path-vbox**
    If you want to override the value of a variable per a specific host, you
    need to suffix it with the host name (in this case, the path will be
    different on vbox host)
**depends**
    module dependencies. Multiple modules should be joined by comma, e.g
    module1,module2,module3

`scm` section:

**url**
    This is a one-line definition of where our source code is located. first
    part (the 'protocol') is mapped to module name inside porter.core.scm
    package, and the rest is passed to it's constructor.

`release` section:

You can have multiple 'releases' inside your project. You **must** prefix them
with `release` name. The key thing to remember here is that if you deploy with
one particular release, all modules will be deployed with this particular
release.

The variables are dependent on what is specified as the scm class. For example,
git repository can be checked out on either a branchname or tag, therefore
both of these keys are allowed here::

    [release:stable]
    branch = release/stable
    tag = my-stable-tag

Deploy!
-------

inside your project directory, execute the following command: ::

    porter-admin deploy --host vbox --config production

And let the magic begin ;)
