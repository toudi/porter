from fabric.operations import local
from fabric.operations import run
from fabric.api import env


RSYNC_SSH_NOAGENT = "ssh -p %(port)s -i %(ident)s"
RSYNC_SSH_AGENT   = "ssh -A -p %(port)s"

def rsync(local_dir, remote_dir, options={}):
    options.update({'-aurz': True})

    ssh_args = {'port': env.port}
    ssh_cmd  = RSYNC_SSH_AGENT

    if hasattr(env, 'key_filename') and not env.forward_agent:
        ssh_cmd = RSYNC_SSH_NOAGENT
        ssh_args['ident'] = env.key_filename

    options["-e"] = ssh_cmd % ssh_args

    rsync_options = []
    for switch, value in options.items():
        if value == True:
            rsync_options.append(switch)
        else:
            rsync_options.append('%s "%s"' % (switch, value))
    return local("rsync %s %s %s" % (
        ' '.join(rsync_options),
        local_dir,
        remote_dir)
    )
