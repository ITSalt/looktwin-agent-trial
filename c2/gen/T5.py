import posixpath


def safe_join(base: str, user_path: str) -> str:
    """
    Join user_path onto base and return the absolute, normalized POSIX path.

    Raises ValueError if:
      - base is not absolute,
      - user_path is absolute (it would discard base),
      - user_path contains a NUL byte,
      - the normalized result is not base itself or located inside base.

    Pure path logic: the filesystem is never accessed, so symlinks are not
    resolved.
    """
    if not isinstance(base, str) or not isinstance(user_path, str):
        raise ValueError("base and user_path must be strings")
    if "\x00" in base or "\x00" in user_path:
        raise ValueError("NUL byte in path")
    if not base:
        raise ValueError("base must not be empty")
    if not posixpath.isabs(base):
        raise ValueError("base must be an absolute path")
    if posixpath.isabs(user_path):
        raise ValueError("user_path must be relative")

    base_norm = posixpath.normpath(base)
    # POSIX normpath preserves exactly two leading slashes; collapse them.
    if base_norm.startswith("//"):
        base_norm = "/" + base_norm.lstrip("/")

    result = posixpath.normpath(posixpath.join(base_norm, user_path))

    if base_norm == "/":
        # Everything absolute is inside the root.
        return result

    if result == base_norm or result.startswith(base_norm + "/"):
        return result

    raise ValueError("path escapes base directory")
