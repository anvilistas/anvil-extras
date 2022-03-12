# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras


import sys
from functools import wraps
from time import time

try:
    import logging

    def get_logger():
        logging.basicConfig(level=logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger = logging.getLogger(__name__)
        logger.addHandler(handler)
        return logger


except ImportError:
    from . import _logging as logging

    def get_logger():
        return logging.Logger(
            name="timing", format="{datetime:%Y-%m-%d %H:%M:%S}: {msg}"
        )


__version__ = "1.9.0"

LOGGER = get_logger()


def _signature(func, args, kwargs):
    sig = [repr(a) for a in args]
    sig.extend(f"{key}={value!r}" for key, value in kwargs.items())
    sig = ",".join(sig)
    if len(sig) > 50:
        sig = sig[:50] + "..."
    return f"{func.__name__}({sig})"


def timed(func, logger=LOGGER, level=logging.INFO):
    @wraps(func)
    def wrapper(*args, **kwargs):
        signature = _signature(func, args, kwargs)
        logger.log(msg=f"{signature} called", level=level)
        started_at = time()
        result = func(*args, **kwargs)
        finished_at = time()
        duration = f"{(finished_at - started_at):.2f}s"
        logger.log(
            msg=f"{signature} completed({duration})",
            level=level,
        )
        return result

    return wrapper
