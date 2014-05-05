from porter.tools.run import run_or_sudo


def sed_replace(replace_dict, path, search_wrapper='__%s__', auto_escape=True, use_sudo=False):
    """
    Executes sed in 'edit-in-place' mode, replacing all of `search`
    occurences with `replace`.
    You need to pass `replace_dict` as a dict, where keys are searches
    and values are replacements.
    
    param auto_escape - specifies whether the values should be searched for '/' and auto escaped
    This is usually a wise thing to do with sed, however if you do it yourself, then set this value
    to false.
    """
    replace_tmpl = "s/%(search)s/%(replace)s/g;"
    sed_cmd      = "sed -i -e'%s' %s"

    r = []

    for search, _replace in replace_dict.items():
        if auto_escape:
            _replace = _replace.replace('/', '\/')
        r.append(replace_tmpl % {
            'search': search_wrapper % search,
            'replace': _replace
        })

    run_or_sudo(sed_cmd % (''.join(r), path), use_sudo)
    del r
