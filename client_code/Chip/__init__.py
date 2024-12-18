# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import HtmlPanel as _HtmlPanel
from anvil.js import get_dom_node as _get_dom_node

from ..utils._component_helpers import _html_injector, _spacing_property
from ._anvil_designer import ChipTemplate

__version__ = "3.1.0"

_html_injector.css(
    """.ae-chip{
    height: 32px;
    font-size: 14px;
    font-weight: 500;
    color: rgba(0,0,0,0.6);
    line-height: 32px;
    padding: 0 12px;
    border-radius: 16px;
    background-color: #e4e4e4;
    display: flex;
    gap: 14px;
    align-items:center;
    width: fit-content;
    padding-left: 12px;
    padding-right: 12px;
    position: relative;
}

.ae-chip i.anvil-component-icon {
    font-size: 1.5rem;
}
.ae-chip a {
    user-select: none;
}
.ae-chip span, .ae-chip a > div {
    padding: 0 !important;
}
"""
)

_defaults = {
    "icon": "",
    "text": "",
    "foreground": "rgba(0,0,0,0.6)",
    "background": "",
    "close_icon": True,
    "spacing_above": "small",
    "spacing_below": "small",
    "visible": True,
}


class Chip(ChipTemplate):
    def __init__(self, **properties):
        dom_node = self._dom_node = _get_dom_node(self)
        dom_node.addEventListener("click", lambda e: self.raise_event("click"))
        dom_node.classList.add("ae-chip")
        dom_node.tabIndex = 0

        self.close_link.set_event_handler(
            "click", lambda **e: self.raise_event("close_click")
        )
        properties = _defaults | properties
        self.init_components(**properties)

        def _spacebar_delete_chip(js_event):
            self.raise_event("close_click")
            js_event.preventDefault()

        _get_dom_node(self.close_link).addEventListener(
            "keydown", _spacebar_delete_chip
        )
        # Any code you write here will run when the form opens.

    @property
    def text(self):
        return self.chip_label.text

    @text.setter
    def text(self, value):
        self.chip_label.text = value

    @property
    def icon(self):
        return self.chip_label.icon

    @icon.setter
    def icon(self, value):
        self.chip_label.icon = value

    @property
    def foreground(self):
        return self.chip_label.foreground

    @foreground.setter
    def foreground(self, value):
        self.chip_label.foreground = value or "rgba(0,0,0,0.6)"
        self.close_link.foreground = value or "rgba(0,0,0,0.6)"

    @property
    def close_icon(self):
        return self.close_link.visible

    @close_icon.setter
    def close_icon(self, value):
        self.close_link.visible = value

    background = _HtmlPanel.background
    visible = _HtmlPanel.visible
    tag = _HtmlPanel.tag
    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")
