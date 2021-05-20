# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
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
# This software is published at https://github.com/anvilistas/anvil-extras


from functools import wraps
from time import gmtime, strftime, time

__version__ = "1.1.0"


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
