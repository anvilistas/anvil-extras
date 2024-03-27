# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import sys
from functools import lru_cache

__version__ = "2.6.1"


def __dir__():
    return [
        "auto_refreshing",
        "ProxyItem",
        "correct_canvas_resolution",
        "import_module",
        "timed",
        "wait_for_writeback",
    ]


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.
    """
    level = 0
    if name.startswith("."):
        if not package:
            msg = (
                "the 'package' argument is required to perform a relative "
                "import for {!r}"
            )
            raise TypeError(msg.format(name))
        for character in name:
            if character != ".":
                break
            level += 1
        if package not in sys.modules:
            # make sure the package exists
            __import__(package, {"__package__": None})

    name = name[level:]
    mod = __import__(name, {"__package__": package}, level=level)
    attrs = name.split(".")[1:]
    for attr in attrs:
        mod = getattr(mod, attr)
    return mod


_imports = {
    "auto_refreshing": "._auto_refreshing",
    "BindingRefreshDict": "._auto_refreshing",
    "ProxyItem": "._auto_refreshing",
    "correct_canvas_resolution": "._canvas_helpers",
    "timed": "._timed",
    "wait_for_writeback": "._writeback_waiter",
}


@lru_cache(maxsize=None)
def __getattr__(name):
    try:
        rel_import = _imports[name]
    except KeyError:
        raise AttributeError(name)

    module = import_module(rel_import, __package__)
    return getattr(module, name)
