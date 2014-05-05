from fabric.operations import run, sudo


def run_or_sudo(cmd, use_sudo):
    if use_sudo:
        sudo(cmd, shell=False)
    else:
        run(cmd)
