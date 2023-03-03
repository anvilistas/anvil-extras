# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import partial

import anvil.js
from anvil import HtmlPanel as _HtmlPanel
from anvil import Link as _Link

from ..utils._component_helpers import (
    _get_color,
    _get_rgb,
    _html_injector,
    _spacing_property,
)
from ._anvil_designer import TabsTemplate

__version__ = "2.2.3"

_html_injector.css(
    """
.anvil-extras-tabs.anvil-role-card {
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}
.tabs {
    position: relative;
    overflow-x: auto;
    overflow-y: hidden;
    height: 48px;
    width: 100%;
    background-color: var(--background, inherit);
    margin: 0 auto;
    white-space: nowrap;
    padding: 0;
    display: flex;
    z-index: 1;
}
.tabs .tab {
    flex-grow: 1;
    display: inline-block;
    text-align: center;
    line-height: 48px;
    height: 48px;
    padding: 0;
    margin: 0;
    text-transform: uppercase
}
.tabs .tab a {
    color: rgba(var(--color),0.7);
    display: block;
    width: 100%;
    height: 100%;
    padding: 0 24px;
    font-size: 14px;
    text-overflow: ellipsis;
    overflow: hidden;
    -webkit-transition: color .28s ease, background-color .28s ease;
    transition: color .28s ease, background-color .28s ease
}
.tabs .tab a:focus,.tabs .tab a:focus.active {
    background-color: rgb(var(--color), 0.2);
    outline: none
}
.tabs .tab a:hover,.tabs .tab a.active {
    background-color: transparent;
    color: rgb(var(--color));
}
.tabs .indicator {
    position: absolute;
    bottom: 0;
    height: 3px;
    background-color: rgb(var(--color), 0.4);
    will-change: left, right;
}
"""
)

_defaults = {
    "align": "left",
    "tab_titles": [],
    "active_tab_index": 0,
    "spacing_above": "none",
    "spacing_below": "none",
    "foreground": "",
    "background": "",
    "role": None,
    "visible": True,
    "bold": False,
    "italic": False,
    "font": None,
    "font_size": None,
}


def _apply_to_links(prop):
    def getter(self):
        return self._props[prop]

    def setter(self, value):
        self._props[prop] = value
        for link in self.get_components():
            setattr(link, prop, value)

    return property(getter, setter)


class Tabs(TabsTemplate):
    def __init__(self, **properties):
        #### set up dom nodes
        dom_node = self._dom_node = anvil.js.get_dom_node(self)
        dom_node.style.padding = "0"
        dom_node.classList.add("anvil-extras-tabs")

        self._tabs_node = dom_node.querySelector(".tabs")
        dom_node.removeChild(dom_node.querySelector("script"))
        self._indicator = self._tabs_node.querySelector(".indicator")

        props = self._props = _defaults | properties

        # annoying font_size property
        if isinstance(props["font_size"], str) and props["font_size"].isdigit():
            props["font_size"] = int(props["font_size"])

        self._prev = props["active_tab_index"]

        props_to_init = {
            "tab_titles": props["tab_titles"],
            "spacing_above": props["spacing_above"],
            "spacing_below": props["spacing_below"],
            "foreground": props["foreground"],
            "background": props["background"],
            "role": props["role"],
            "visible": props["visible"],
        }

        self.init_components(**props_to_init)
        # do this on the link element incase the user has already set the form show event
        link_0 = self.get_components()[0]
        if link_0:
            link_0.set_event_handler("show", lambda **e: self._set_indicator())

    def _raise_tab_click(self, sender, tab_index, **event_args):
        self._set_indicator(tab_index)
        self.raise_event(
            "tab_click",
            tab_index=tab_index,
            tab_title=sender.text,
            tab_component=sender,
        )

    def _set_indicator(self, tab_index=None):
        tab_index = tab_index if tab_index is not None else self._prev

        for i, node in enumerate(self._link_nodes):
            node.classList.toggle("active", i == tab_index)

        left, right = (0, 90) if tab_index <= self._prev else (90, 0)
        self._indicator.style.transition = (
            f"left 300ms ease-out {left}ms, right 300ms ease-out {right}ms"
        )

        self._prev = tab_index
        link_node = self._link_nodes[tab_index]
        left = link_node.offsetLeft
        right = (
            self._tabs_node.offsetWidth - link_node.offsetLeft - link_node.offsetWidth
        )
        self._indicator.style.left = f"{left}px"
        self._indicator.style.right = f"{right}px"

    @property
    def tab_titles(self):
        return self._props["tab_titles"]

    @tab_titles.setter
    def tab_titles(self, tab_list):
        self._props["tab_titles"] = tab_list or []
        self.clear()
        self._link_nodes = []
        for i, text in enumerate(tab_list):
            link = _Link(
                text=text,
                spacing_above="none",
                spacing_below="none",
                align=self.align,
                bold=self.bold,
                italic=self.italic,
                font=self.font,
                font_size=self.font_size,
            )
            link.set_event_handler("click", partial(self._raise_tab_click, tab_index=i))
            self._link_nodes.append(anvil.js.get_dom_node(link))
            self.add_component(link)
        self._set_indicator()

    @property
    def active_tab_index(self):
        return self._prev

    @active_tab_index.setter
    def active_tab_index(self, index):
        self._set_indicator(index)

    @property
    def foreground(self):
        return self._props["foreground"]

    @foreground.setter
    def foreground(self, value):
        self._props["foreground"] = value
        self._dom_node.style.setProperty("--color", _get_rgb(value))

    @property
    def background(self):
        return self._props["background"]

    @background.setter
    def background(self, value):
        self._props["background"] = value
        self._dom_node.style.setProperty("--background", value and _get_color(value))

    align = _apply_to_links("align")
    bold = _apply_to_links("bold")
    font = _apply_to_links("font")
    font_size = _apply_to_links("font_size")
    italic = _apply_to_links("italic")

    role = _HtmlPanel.role
    visible = _HtmlPanel.visible
    tag = _HtmlPanel.tag
    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")
