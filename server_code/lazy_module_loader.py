# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "2.2.3"


def __getattr__(name):
    try:
        mod = __import__(name)
    except ImportError:
        raise AttributeError(name)
    globals()[name] = mod
    return mod
