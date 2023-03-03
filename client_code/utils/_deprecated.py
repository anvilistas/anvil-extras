# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import wraps

__version__ = "2.2.3"


def deprecated(msg=""):
    def outer(fn):
        # nonlocal not available
        warned = [False]

        @wraps(fn)
        def wrapper(*args, **kws):
            if not warned[0]:
                warned[0] = True
                print("DeprecatedWarning:", msg)

            return fn(*args, **kws)

        return wrapper

    return outer
