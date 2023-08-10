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
        self._resolve = resolve
        if not self._pending:
            resolve()

    def __init__(self):
        self._promise = None
        self._resolve = None
        self._pending = True

    @property
    def promise(self):
        if self._promise is None:
            self._promise = _window.Promise(self.init_promise)
        return self._promise

    def resolve(self, value=None):
        self._pending = False
        if self._resolve is not None:
            self._resolve(value)


class _WritebackWaiter:
    def __init__(self):
        self.deferred = _Deferred()

    def __enter__(self):
        _active_writebacks.append(self.deferred)

    def __exit__(self, exc, *args):
        global _active_writebacks
        deferred = self.deferred
        _active_writebacks = [d for d in _active_writebacks if d is not deferred]
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
        _window.Promise.allSettled([d.promise for d in _active_writebacks])
        return fn(self, *args, **kws)

    return wrapper
