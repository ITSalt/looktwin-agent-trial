import re

_PATTERN = re.compile(
    r"""
    (?P<prefix>
        (?<!\w)
        (?:password|token|api_key|secret)
        ["']?                 # optional closing quote of the key (JSON)
        [ \t]*[:=][ \t]*      # separator
    )
    (?P<value>
        "(?:[^"\\]|\\.)*"     # double-quoted value
      | '(?:[^'\\]|\\.)*'     # single-quoted value
      | [^\s,;&}\]]+          # unquoted value
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _replace(match: re.Match) -> str:
    prefix = match.group("prefix")
    value = match.group("value")
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        q = value[0]
        return f"{prefix}{q}***{q}"
    return f"{prefix}***"


def mask_secrets(text: str) -> str:
    return _PATTERN.sub(_replace, text)
