# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import cache

__version__ = "1.7.1"


def __dir__():
    return ["auto_refreshing", "wait_for_writeback", "timed", "BindingRefreshDict"]


@cache
def __getattr__(name):
    # todo use dynamic imports but __import__ is not yet supported in skult
    if name == "auto_refreshing":
        from ._auto_refreshing import auto_refreshing

        return auto_refreshing
    elif name == "timed":
        from ._timed import timed

        return timed
    elif name == "wait_for_writeback":
        from ._writeback_waiter import wait_for_writeback

        return wait_for_writeback
    elif name == "BindingRefreshDict":
        from ._auto_refreshing import BindingRefreshDict

        return BindingRefreshDict
    else:
        raise AttributeError(name)
