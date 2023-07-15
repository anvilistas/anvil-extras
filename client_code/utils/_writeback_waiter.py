# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import wraps as _wraps
from time import sleep as _sleep

from anvil import Component as _Component
from anvil.js import window as _window

__version__ = "2.4.0"

_active_writebacks = []


class _Deferred:
    def init_promise(self, resolve, reject):
        self.resolve = resolve
        self.reject = reject

    def __init__(self):
        self.promise = _window.Promise(self.init_promise)


class _WritebackWaiter:
    def __init__(self):
        self.deferred = _Deferred()

    def __enter__(self):
        _active_writebacks.append(self.deferred.promise)

    def __exit__(self, exc, *args):
        global _active_writebacks
        promise = self.deferred.promise
        _active_writebacks = [p for p in _active_writebacks if p is not promise]
        self.deferred.resolve()


_old_raise = _Component.raise_event


def raise_event(self, event_name, **kws):
    if not event_name.startswith("x-anvil-write-back"):
        return _old_raise(self, event_name, **kws)
    with _WritebackWaiter():
        return _old_raise(self, event_name, **kws)


_Component.raise_event = raise_event


def wait_for_writeback(fn):
    @_wraps(fn)
    def wrapper(self, *args, **kws):
        _sleep(0)
        _window.Promise.allSettled(_active_writebacks)
        return fn(self, *args, **kws)

    return wrapper
