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

from functools import cache

__version__ = "1.2.0"


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
