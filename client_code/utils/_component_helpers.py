# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import random

import anvil.js
from anvil import Component as _Component
from anvil import app as _app
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import Promise as _Promise
from anvil.js.window import document as _document

__version__ = "2.4.0"

_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class HTMLInjector:
    _injected_css = set()

    def css(self, css):
        """inject some custom css"""
        hashed = hash(css)
        if hashed in self._injected_css:
            return
        sheet = self._create_tag("style")
        sheet.innerHTML = css
        self._inject(sheet, head=False)
        self._injected_css.add(hashed)

    def cdn(self, cdn_url, **attrs):
        """inject a js/css cdn file"""
        if cdn_url.endswith("js"):
            tag = self._create_tag("script", src=cdn_url, **attrs)
        elif cdn_url.endswith("css"):
            tag = self._create_tag("link", href=cdn_url, rel="stylesheet", **attrs)
        else:
            raise ValueError("Unknown CDN type expected css or js file")
        self._inject(tag)
        self._wait_for_load(tag)

    def script(self, js):
        """inject some javascript code inside a script tag"""
        s = self._create_tag("script")
        s.textContent = js
        self._inject(s)

    def _create_tag(self, tag_name, **attrs):
        tag = _document.createElement(tag_name)
        for attr, value in attrs.items():
            tag.setAttribute(attr, value)
        return tag

    def _inject(self, tag, head=True):
        if head:
            _document.head.appendChild(tag)
        else:
            _document.body.appendChild(tag)

    def _wait_for_load(self, tag):
        if not tag.get("src"):
            return

        def do_wait(res, rej):
            tag.onload = res
            tag.onerror = rej

        p = _Promise(do_wait)
        anvil.js.await_promise(p)


_html_injector = HTMLInjector()


def _get_dom_node_id(component):
    node = _get_dom_node(component)
    if not node.id:
        node.id = "".join([random.choice(_characters) for _ in range(8)])
    return node.id


def _spacing_property(a_b):
    def getter(self):
        return getattr(self, "_spacing_" + a_b)

    def setter(self, value):
        self._dom_node.classList.remove(
            f"anvil-spacing-{a_b}-{getattr(self, '_spacing_' + a_b, '')}"
        )
        self._dom_node.classList.add(f"anvil-spacing-{a_b}-{value}")
        setattr(self, "_spacing_" + a_b, value)

    return property(getter, setter, None, a_b)


_primary = _app.theme_colors.get("Primary 500", "#2196F3")


def _get_color(value):
    if not value:
        return _primary
    elif value.startswith("theme:"):
        return _app.theme_colors.get(value.replace("theme:", ""), _primary)
    else:
        return value


def _get_rgb(value):
    value = _get_color(value)
    if value.startswith("#"):
        value = value[1:]
        value = ",".join(str(int(value[i : i + 2], 16)) for i in (0, 2, 4))
    elif value.startswith("rgb") and value.endswith(")"):
        value = value[value.find("("), -1]
    else:
        raise ValueError(
            f"expected a hex value, theme color or rgb value, not, {value}"
        )
    return value


def _walker(children):
    for child in children:
        yield child
        get_children = getattr(child, "get_components", None)
        if get_children is not None:
            yield from _walker(get_children())


def walk(component_or_components):
    """yields the component(s) passed in and all their children"""
    if isinstance(component_or_components, _Component):
        component_or_components = [component_or_components]
    yield from _walker(component_or_components)


def _css_length(v):
    try:
        return f"{float(v)}px"
    except (TypeError, ValueError):
        return v
