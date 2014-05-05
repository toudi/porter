from importlib import import_module


def get_scm_instance(url, module):
    scm_module, scm_url = url.split('://')
    return import_module(
        'porter.core.scm.%s' % scm_module
    ).SCM(scm_url, module)
