from fabric.operations import local
from fabric.api import env
import os.path
from fabric.contrib.files import exists as rexists


CMD_AGENT   = "scp -P %(port)s %(local_file)s %(user)s@%(host)s:%(remote_file)s"
CMD_NOAGENT = "scp -P %(port)s -i %(ident)s %(local_file)s %(user)s@%(host)s:%(remote_file)s"


def scp(local_file, remote_file, copy_if_exists=False):
    args = {
        "port": env.port,
        "local_file": local_file,
        "user": env.user,
        "host": env.host,
        "remote_file": remote_file
    }

    if os.path.isdir(local_file):
        args['local_file'] = '-r %s' % local_file

    cmd = CMD_AGENT

    if not env.forward_agent:
        cmd = CMD_NOAGENT
        args['ident'] = env.key_filename

    if not rexists(remote_file) or copy_if_exists:
        return local(cmd % args)