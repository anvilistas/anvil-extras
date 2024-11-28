# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "3.1.0"

__all__ = ["EMAIL", "UUID", "URL"]  # noqa: F822


_raw = {
    "EMAIL": r"^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$",
    "UUID": r"([a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[a-f0-9]{4}-[a-f0-9]{12}|00000000-0000-0000-0000-000000000000)$",
    # https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
    "URL": (
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$"
    ),
}

_cache = {}


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)

    # do this lazily on the client
    import re

    _cache[name] = re.compile(_raw[name], re.IGNORECASE)

    return _cache[name]


def __dir__(self):
    return __all__
