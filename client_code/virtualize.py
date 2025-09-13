# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil
from anvil.js import import_from, window

__version__ = "3.4.0"

if window.get("tanstackvirtualCore"):
    virtual_core = window.tanstackvirtualCore
else:
    virtual_core = import_from(
        "https://cdn.jsdelivr.net/npm/@tanstack/virtual-core@3.13.12/+esm"
    )


def noop(*args, **kwargs):
    pass


class Virtualizer:
    def __init__(
        self,
        count,
        component,
        scroll_element,
        estimate_size,
        on_change=None,
        get_item_key=None,
    ):
        assert isinstance(component, anvil.Component)
        assert callable(estimate_size)
        self._on_change = on_change

        self._opts = {
            "count": count,
            "getScrollElement": lambda: scroll_element,
            "estimateSize": estimate_size,
            "scrollToFn": virtual_core.elementScroll,
            "observeElementOffset": virtual_core.observeElementOffset,
            "observeElementRect": virtual_core.observeElementRect,
            "onChange": self.on_change,
        }

        if get_item_key:
            self._opts["getItemKey"] = get_item_key

        self.cleanup = noop

        self._virtualizer = virtual_core.Virtualizer(self._opts)

        component.add_event_handler("x-anvil-page-added", self._page_added)
        component.add_event_handler("x-anvil-page-removed", self._page_removed)

    def _page_added(self, *args, **kwargs):
        self.cleanup = self._virtualizer._didMount()
        self._virtualizer._willUpdate()

    def _page_removed(self, *args, **kwargs):
        self.cleanup()

    def update(self, count=0):
        self._opts["count"] = count
        self._virtualizer.setOptions(self._opts)

    def scroll_to_index(self, index, align="auto"):
        self._virtualizer.scrollToIndex(index, {"align": align})

    def get_virtual_items(self):
        return self._virtualizer.getVirtualItems()

    def get_total_size(self):
        return self._virtualizer.getTotalSize()

    def on_change(self, *args):
        on_change = self._on_change
        if callable(on_change):
            on_change()
