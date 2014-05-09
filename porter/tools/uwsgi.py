from fabric.operations import run


def restart(pidfile):
    run('kill -HUP `cat %s`' % pidfile)
