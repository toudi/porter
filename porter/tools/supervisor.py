from porter.tools.scp import scp
from porter.tools.sed import sed_replace
from porter.tools.run import run_or_sudo
from os.path import basename


def SUPERVISORCTL_COMMAND(cmd, cfg=None):
    if cfg:
        cfg = '-c '+cfg
    return "supervisorctl %(cfg)s%(command)s" % {'cfg': cfg or '', 'command': cmd}


def restart(name, cfg=None, use_sudo=False):
    run_or_sudo(SUPERVISORCTL_COMMAND("restart %s" % name, cfg), use_sudo)

def start(name, cfg=None, use_sudo=False):
    run_or_sudo(SUPERVISORCTL_COMMAND("start %s" % name, cfg), use_sudo)

def stop(name, cfg=None, use_sudo=False):
    run_or_sudo(SUPERVISORCTL_COMMAND("stop %s" % name, cfg), use_sudo)

def stop_group(group, cfg=None, use_sudo=False):
    stop("%s:*" % group, cfg, use_sudo)

def start_group(group, cfg=None, use_sudo=False):
    start("%s:*" % group, cfg, use_sudo)

def reload_cfg(cfg=None, use_sudo=False):
    run_or_sudo(SUPERVISORCTL_COMMAND("update", cfg), use_sudo)

def update_supervisor_launcher(
    source_location,
    dest_location='/etc/supervisor/conf.d/',
    use_sudo=False,
    replace_dict=None
):
    scp(source_location, dest_location, use_sudo)
    sed_replace(replace_dict, '%s/%s' % (dest_location, basename(source_location)), use_sudo=use_sudo)
