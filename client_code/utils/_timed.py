# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras


import sys
from functools import wraps
from time import time

from .. import logging as logging

__version__ = "2.2.3"

LOGGER = logging.Logger(name="timing", format="{datetime:%Y-%m-%d %H:%M:%S}: {msg}")


def _signature(func, args, kwargs):
    """Text representation of a function's signature"""
    sig = [repr(a) for a in args]
    sig.extend(f"{key}={value!r}" for key, value in kwargs.items())
    sig = ",".join(sig)
    if len(sig) > 40:
        sig = sig[:40] + "..."

    return f"{func.__name__}({sig})"


def timed(_func=None, *, logger=LOGGER, level=logging.INFO):
    """A decorator to time the execution of a function"""
    if _func is None:
        return lambda _func: timed(_func, logger=logger, level=level)

    @wraps(_func)
    def wrapper(*args, **kwargs):
        signature = _signature(_func, args, kwargs)
        logger.log(msg=f"{signature} called", level=level)
        started_at = time()
        result = _func(*args, **kwargs)
        finished_at = time()
        duration = f"{(finished_at - started_at):.2f}s"
        logger.log(
            msg=f"{signature} completed({duration})",
            level=level,
        )
        return result

    return wrapper
