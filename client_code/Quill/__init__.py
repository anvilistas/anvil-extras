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

from ..utils._component_helpers import _add_script, _spacing_property
from ._anvil_designer import QuillTemplate

__version__ = "1.5.1"

# <!-- Theme included stylesheets -->
_add_script('<link href="//cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">')
_add_script('<link href="//cdn.quilljs.com/1.3.6/quill.bubble.css" rel="stylesheet">')

# <!-- Main Quill library -->
_add_script('<script src="//cdn.quilljs.com/1.3.6/quill.min.js"></script>')
_Quill = _window.Quill


_defaults = {
    "auto_expand": True,
    "content": None,
    "enabled": True,
    "height": 150,
    "placeholder": None,
    "readonly": False,
    "spacing_above": "small",
    "spacing_below": "small",
    "theme": "snow",
    "toolbar": True,
    "visible": True,
}


def _quill_init_prop(propname):
    def getter(self):
        return self._props[propname]

    def setter(self, val):
        self._props[propname] = val
        self._init_quill()

    return property(getter, setter)


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
                "modules": {"toolbar": self._props["toolbar"]},
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
            self.set_html(html)

    def __getattr__(self, name):
        init, *rest = name.split("_")
        name = init + "".join(map(str.title, rest))
        return getattr(self._quill, name)

    #### Properties ####
    @property
    def enabled(self):
        return self._props["enabled"]

    @enabled.setter
    def enabled(self, value):
        self._quill.enable(bool(value))
        self._props["enabled"] = value

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

    @property
    def auto_expand(self):
        return self._props["auto_expand"]

    @auto_expand.setter
    def auto_expand(self, value):
        self._props["auto_expand"] = value
        self._spacer.height = "auto" if value else self._min_height

    @property
    def height(self):
        return self._props["height"]

    @height.setter
    def height(self, value):
        self._props["height"] = value
        if isinstance(value, (int, float)) or value.isdigit():
            value = f"{value}px"
        self._el.style.minHeight = value
        self._min_height = value

    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")
    visible = _HtmlPanel.visible

    #### QUILL INIT PROPS ####
    toolbar = _quill_init_prop("toolbar")
    readonly = _quill_init_prop("readonly")
    theme = _quill_init_prop("theme")
    placeholder = _quill_init_prop("placeholder")

    #### ANVIL METHODS ####
    def get_markdown(self):
        """Not yet implemented"""
        # https://github.com/frysztak/quill-delta-to-markdown/tree/master/src
        # https://github.com/leforestier/yattag
        raise NotImplementedError("get_markdown() has not yet been implemented")

    def get_html(self):
        """convert the contents of the quill object to html which can be used
        as the content to a RichText editor in 'restricted_html' format
        Can also be used as a classmethod by calling it with a simple object Quill.to_html(content)"""
        return self._quill and self._quill.root.innerHTML

    def set_html(self, html):
        """set the content to html. This method sanitizes the html
        in the same way the RichText compeonent does"""
        self._rt = self._rt or _RT(visible=False, format="restricted_html")
        self._rt.content = html
        html = _get_dom_node(self._rt).innerHTML
        self._quill.root.innerHTML = html
