# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import cache

__version__ = "1.9.0"


def __dir__():
    return [
        "auto_refreshing",
        "wait_for_writeback",
        "timed",
        "logging",
        "BindingRefreshDict",
        "correct_canvas_resolution",
    ]


@cache
def __getattr__(name):
    # todo use dynamic imports but __import__ is not yet supported in skulpt
    if name == "auto_refreshing":
        from ._auto_refreshing import auto_refreshing

        return auto_refreshing
    elif name == "timed":
        from ._timed import timed

        return timed
    elif name == "logging":
        from . import _logging

        return _logging
    elif name == "wait_for_writeback":
        from ._writeback_waiter import wait_for_writeback

        return wait_for_writeback
    elif name == "BindingRefreshDict":
        from ._auto_refreshing import BindingRefreshDict

        return BindingRefreshDict
    elif name == "correct_canvas_resolution":
        from ._canvas_helpers import correct_canvas_resolution

        return correct_canvas_resolution
    else:
        raise AttributeError(name)
