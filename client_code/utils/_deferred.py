# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js import window as _window

__version__ = "2.6.2"


class Deferred:
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
