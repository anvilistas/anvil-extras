# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import random

import anvil.js
from anvil import Component as _Component
from anvil import TextBox as _TextBox
from anvil import app as _app
from anvil.js import get_dom_node as _get_dom_node
from anvil.js import window
from anvil.js.window import Promise as _Promise
from anvil.js.window import document as _document

__version__ = "3.5.0"

_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
window.anvilExtras = window.get("anvilExtras", {})
window.anvilExtras["injectedHtml"] = window.anvilExtras.get("injectedHtml", {})
_injectedHtml = window.anvilExtras["injectedHtml"]


class HTMLInjector:
    def _is_injected(self, text, type):
        hashed = hash((type, text))
        if hashed in _injectedHtml:
            return True
        _injectedHtml[hashed] = True
        return False

    def css(self, css):
        """inject some custom css"""
        if self._is_injected(css, "css"):
            return
        sheet = self._create_tag("style")
        sheet.innerHTML = css
        self._inject(sheet, head=False)

    def cdn(self, cdn_url, **attrs):
        """inject a js/css cdn file"""
        if self._is_injected(cdn_url, "cdn"):
            return
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
        if self._is_injected(js, "script"):
            return
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


_primary_color = (window.document.querySelector("meta[name=theme-color]") or {}).get(
    "content", "#2196F3"
)


def _supports_relative_colors():
    return window.CSS.supports("color", "rgb(from white r g b / 0.2)")


_tb = _TextBox()
_tb_node = _get_dom_node(_tb)


def _get_color(value):
    if not value:
        return _primary_color

    _tb.foreground = value
    color = _tb_node.style.color

    if color.startswith("--"):
        return f"var({color})"

    return color


_hidden_style_getter = None


def _get_computed_color(value):
    global _hidden_style_getter
    if _hidden_style_getter is None:
        container = _document.createElement("div")
        container.style.display = "none"
        container.style.color = "chartreuse"  # obscure color
        _hidden_style_getter = _document.createElement("div")
        container.appendChild(_hidden_style_getter)
        _document.body.appendChild(container)

    _hidden_style_getter.style.color = ""
    _hidden_style_getter.style.color = value

    computed = window.getComputedStyle(_hidden_style_getter).color
    if computed == "rgb(127, 255, 0)":
        return value
    else:
        return computed


def _strip_rgba(value):
    original = value

    value = value.strip()

    if value.startswith("rgba("):
        value = value[5:]

    if value.startswith("rgb("):
        value = value[4:]

    if value.endswith(")"):
        value = value[:-1]

    value = value.split(",")

    if len(value) == 3:
        return " ".join(v.strip() for v in value)

    if len(value) == 4:
        return f"{value[0].strip()} {value[1].strip()} {value[2].strip()} / {value[3].strip()}"

    return original


def _get_rgb(value):
    value = _get_color(value)
    value = _get_computed_color(value)
    value = _strip_rgba(value)
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


def _ensure_role_is_list(role):
    if role is None:
        return []

    if isinstance(role, str):
        return [role]

    return role


def _add_roles(self, roles):
    current_roles = _ensure_role_is_list(self.role)
    new_roles = _ensure_role_is_list(roles)

    for role in new_roles:
        if role not in current_roles:
            current_roles.append(role)

    self.role = current_roles


def _remove_roles(self, roles):
    current_roles = _ensure_role_is_list(self.role)
    roles_to_remove = _ensure_role_is_list(roles)

    updated_roles = [role for role in current_roles if role not in roles_to_remove]

    self.role = updated_roles


def _to_kebab(s: str) -> str:
    return "".join(("-" + c.lower()) if c.isupper() else c for c in s).lstrip("-")


def _normalize_attr_name(attr_name: str) -> str:
    if attr_name == "className":
        return "class"
    if attr_name == "htmlFor":
        return "for"
    return _to_kebab(attr_name)


def crelt(node_type: str, **attrs):
    el = _document.createElement(node_type)

    for attr, value in attrs.items():
        if value is None:
            continue
        norm_name = _normalize_attr_name(attr)
        el.setAttribute(norm_name, value)

    return el
