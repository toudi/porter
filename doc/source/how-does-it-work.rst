How does the deployment process work?
=====================================

Whenever you are doing a deployment, the following things occur:

#. porter parses your project.ini file
#. it looks for a list of modules to be deployed
#. it recursively builds dependencies to be deployed, and it starts with them.

For each of the modules, porter does the following things:

#. it parses the module's ini file in order to discover which plugins you are
   using.
#. It checks whether a deploy is actually needed - it uses release section for
   that. If an combination of (module, config, host, release) is found within
   porter.db, then the deployment is not performed.
#. it clones / refreshes the repository
#. it sets the appropriate branch / tag / revision / etc
#. it uses rsync to push your code to the destination machine
#. it stores the deployed version of the module into the porter.db
