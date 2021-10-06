# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras


from functools import wraps
from time import gmtime, strftime, time

__version__ = "1.7.1"


def _signature(func, args, kwargs):
    """Text representation of a function's signature"""
    arguments = [str(a) for a in args]
    arguments.extend([f"{key}={value}" for key, value in kwargs.items()])
    return f"{func.__name__}({','.join(arguments)})"


def _timestamp(seconds):
    """Text representation of a unix timestamp"""
    return strftime("%Y-%m-%d %H:%M:%S", gmtime(seconds))


def timed(func):
    """A decorator to time the execution of a function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        signature = _signature(func, args, kwargs)
        started_at = time()
        print(f"{_timestamp(started_at)} {signature} called")
        result = func(*args, **kwargs)
        finished_at = time()
        duration = f"{(finished_at - started_at):.2f}s"
        print(f"{_timestamp(finished_at)} {signature} completed({duration})")
        return result

    return wrapper
