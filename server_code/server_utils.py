# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import logging
import sys
from functools import wraps
from time import time

__version__ = "1.6.0"


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


LOGGER = get_logger()


def _signature(func, args, kwargs):
    arguments = [str(a) for a in args]
    arguments.extend([f"{key}={value}" for key, value in kwargs.items()])
    return f"{func.__name__}({','.join(arguments)})"


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
