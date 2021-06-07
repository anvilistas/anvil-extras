# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import random

from anvil import app as _app
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S

__version__ = "1.4.0"

_loaded = False
_characters = "abcdefghijklmnopqrstuvwxyz0123456789"


class StyleInjector:
    def __init__(self):
        self.injected = set()

    def inject(self, css):
        hashed = hash(css)
        if hashed not in self.injected:
            sheet = _document.createElement("style")
            sheet.innerHTML = css
            _document.body.appendChild(sheet)
            self.injected.add(hashed)


def _get_dom_node_id(component):
    node = _get_dom_node(component)
    if not node.id:
        node.id = "".join([random.choice(_characters) for _ in range(8)])
    return node.id


def _onload(e):
    global _loaded
    _loaded = True


def _wait_for_load(interval=0.005):
    global _loaded
    while not _loaded:
        from time import sleep

        sleep(interval)
    _loaded = False


def _add_script(s):
    dummy = _S(s)[0]  # let jquery pass the tag
    s = _document.createElement(dummy.tagName)
    for attr in dummy.attributes:
        s.setAttribute(attr.name, attr.value)
    s.textContent = dummy.textContent
    _document.head.appendChild(s)
    if not s.get("src"):
        return
    s.onload = s.onerror = _onload  # ignore errors
    _wait_for_load()


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
