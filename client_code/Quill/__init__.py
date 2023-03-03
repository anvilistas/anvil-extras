# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import HtmlPanel as _HtmlPanel
from anvil import RichText as _RT
from anvil import Spacer as _Spacer
from anvil.js import get_dom_node as _get_dom_node
from anvil.js import window as _window

from ..utils._component_helpers import _html_injector, _spacing_property
from ._anvil_designer import QuillTemplate

__version__ = "2.2.3"

# <!-- Theme included stylesheets -->
prefix = "//cdn.quilljs.com/"
quill_version = "1.3.6"

_html_injector.cdn(f"{prefix}{quill_version}/quill.snow.css")
_html_injector.cdn(f"{prefix}{quill_version}/quill.bubble.css")

# <!-- Main Quill library -->
if _window.get("Quill") is None:
    # support including Quill in the native libraries for easier module imports
    _html_injector.cdn(f"{prefix}{quill_version}/quill.min.js")
_Quill = _window.Quill


_defaults = {
    "auto_expand": True,
    "content": None,
    "enabled": True,
    "height": 150,
    "modules": None,
    "placeholder": None,
    "readonly": False,
    "spacing_above": "small",
    "spacing_below": "small",
    "sanitize": True,
    "theme": "snow",
    "toolbar": True,
    "visible": True,
}


def _quill_prop(propname, setter=None):
    def prop_getter(self):
        return self._props[propname]

    def prop_setter(self, value):
        self._props[propname] = value
        if setter is not None:
            setter(self, value)

    return property(prop_getter, prop_setter)


def _quill_init_prop(propname):
    def setter(self, _value):
        self._init_quill()

    return _quill_prop(propname, setter)


class Quill(QuillTemplate):
    _quill = None  # otherwise we get a recursion error from __getattr__

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self._dom_node = _get_dom_node(self)
        self._spacer = _Spacer()
        self._el = _get_dom_node(self._spacer)
        self._quill = None
        self._rt = None
        self._min_height = None

        def click_guard(e):
            q = self._quill
            if not q.hasFocus():
                q.focus()
                q.setSelection(len(q.getText()))

        self._el.addEventListener("click", click_guard)

        self._props = props = _defaults | properties
        props_to_init = {
            key: props[key]
            for key in (
                "height",
                "content",
                "auto_expand",
                "spacing_above",
                "spacing_below",
            )
        }
        init_if_false = {
            key: props[key] for key in ("enabled", "visible") if not props[key]
        }
        self._init_quill()
        self.init_components(**props_to_init, **init_if_false)

    @staticmethod
    def _clear_elements(el):
        while el.firstElementChild:
            el.removeChild(el.firstElementChild)

    def _init_quill(self):
        html = self.get_html()

        self._spacer.remove_from_parent()
        self._clear_elements(self._dom_node)
        self._clear_elements(self._el)
        self.add_component(self._spacer)

        # these properties have to be set for initialization and cannot be changed
        # If they are changed at runtime we need to create a new quill object
        q = self._quill = _Quill(
            self._el,
            {
                "modules": {"toolbar": self._props["toolbar"]}
                | (self._props["modules"] or {}),
                "theme": self._props["theme"],
                "placeholder": self._props["placeholder"],
                "readOnly": self._props["readonly"],
                "bounds": self._dom_node,
            },
        )

        #### EVENTS ####
        q.on(
            "text-change",
            lambda delta, old_delta, source: self.raise_event(
                "text_change", delta=delta, old_delta=old_delta, source=source
            ),
        )
        q.on(
            "selection-change",
            lambda range, old_range, source: self.raise_event(
                "selection_change", range=range, old_range=old_range, source=source
            ),
        )

        if html:
            self.set_html(html, False)

    def __getattr__(self, name):
        init, *rest = name.split("_")
        name = init + "".join(map(str.title, rest))
        return getattr(self._quill, name)

    #### Properties ####
    def _set_enabled(self, value):
        self._quill.enable(bool(value))

    def _set_auto_expand(self, value):
        self._spacer.height = "auto" if value else self._min_height

    def _set_height(self, value):
        if isinstance(value, (int, float)) or value.isdigit():
            value = f"{value}px"
        self._el.style.minHeight = value
        self._min_height = value

    @property
    def content(self):
        # NB: since each quill object is only one level deep we can just call __serialize__
        # We could just return the proxyobjects but probably nicer to turn them into python dicts here
        return list(map(lambda x: x.__serialize__({}), self._quill.getContents().ops))

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            return self._quill.setText(value)
        self._quill.setContents(value)

    enabled = _quill_prop("enabled", _set_enabled)
    auto_expand = _quill_prop("auto_expand", _set_auto_expand)
    height = _quill_prop("height", _set_height)
    sanitize = _quill_prop("sanitize")
    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")
    visible = _HtmlPanel.visible
    tag = _HtmlPanel.tag

    #### QUILL INIT PROPS ####
    toolbar = _quill_init_prop("toolbar")
    readonly = _quill_init_prop("readonly")
    theme = _quill_init_prop("theme")
    placeholder = _quill_init_prop("placeholder")
    modules = _quill_init_prop("modules")

    #### ANVIL METHODS ####
    def get_markdown(self):
        """Not yet implemented"""
        # https://github.com/frysztak/quill-delta-to-markdown/tree/master/src
        # https://github.com/leforestier/yattag
        raise NotImplementedError("get_markdown() has not yet been implemented")

    def get_html(self):
        """convert the contents of the quill object to html which can be used
        as the content to a RichText editor in 'restricted_html' format
        Can also be used as a classmethod by calling it with a simple object Quill.to_html(content)
        """
        return self._quill and self._quill.root.innerHTML

    def set_html(self, html, sanitize=None):
        """set the content to html. This method sanitizes the html
        in the same way the RichText compeonent does"""
        if sanitize is None:
            sanitize = self._props["sanitize"]
        if sanitize:
            self._rt = self._rt or _RT(visible=False, format="restricted_html")
            self._rt.content = html
            html = _get_dom_node(self._rt).innerHTML
        self._quill.root.innerHTML = html
