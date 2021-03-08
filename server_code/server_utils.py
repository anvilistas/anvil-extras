# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/meatballs/anvil-extras/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/meatballs/anvil-extras
import logging
import sys
from functools import wraps
from time import time

__version__ = "0.1.9"


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
            msg=f"{signature} completed({duration})", level=level,
        )
        return result

    return wrapper
