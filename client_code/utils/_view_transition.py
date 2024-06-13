# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from time import sleep

from anvil.js.window import document, setTimeout

from ._deferred import Deferred

__version__ = "2.6.2"

_transition = None
_can_transition = hasattr(document, "startViewTransition")
_use_transition = True


def use_transitions(can_transition=True):
    global _use_transition
    _use_transition = can_transition


class ViewTransition:
    def __init__(self, form):
        self.deferred = Deferred()
        self.form = form
        self.transition = None
        try:
            handlers = form.get_event_handlers("show")
            form.set_event_handler("show", self.show)
            # make us the first show event handler and re-add existing
            for handler in handlers:
                form.add_event_handler("show", handler)
        except Exception:
            pass

    def resolve(self):
        global _transition
        if _transition is self.transition:
            _transition = None
        self.deferred.resolve(None)

    def show(self, **event_args):
        self.resolve()
        try:
            self.form.remove_event_handler("show", self.show)
        except Exception:
            pass

    def __enter__(self):
        global _transition
        if _transition is None and _can_transition and _use_transition:
            self.transition = document.startViewTransition(
                lambda: self.deferred.promise
            )
            _transition = self.transition
            sleep(0)
            setTimeout(self.resolve, 100)
        return self

    def __exit__(self, *exc_args):
        self.resolve()
