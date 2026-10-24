import posixpath
def safe_join(base, user_path):
    b = posixpath.normpath(posixpath.abspath(base))
    if posixpath.isabs(user_path): raise ValueError
    r = posixpath.normpath(posixpath.join(b, user_path))
    if r != b and not r.startswith(b + '/'): raise ValueError
    return r
