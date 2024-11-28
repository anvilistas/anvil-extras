# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "3.1.0"

_warnings = {}


def warn(key, msg, type="WARNING"):
    if _warnings.get(key):
        return
    _warnings[key] = True
    print(f"{type}: {msg}")
