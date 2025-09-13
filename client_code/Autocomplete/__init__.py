# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import LinearPanel as _LinearPanel
from anvil import Link as _Link
from anvil import pluggable_ui as _pluggable_ui
from anvil.designer import get_design_component
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S
from anvil.js.window import window as _window

from ..utils._component_helpers import _html_injector
from ..virtualize import Virtualizer

__version__ = "3.4.0"


_html_injector.css(
    """
.anvil-role-ae-autocomplete {
    padding: 0 !important;
}
.anvil-role-ae-autocomplete > ul {
    position: relative;
}
.anvil-role-ae-autocomplete > ul > li {
    position: absolute;
    width: 100%;
    left: 0;
    right: 0;
}
.anvil-role-ae-autocomplete {
    position: absolute;
    transform: scaleX(1) scaleY(1);
    opacity: 1;
    transform-origin: 0px 0px;
    overflow-y: auto;
    min-width: 100px;
    max-height: 300px;
    transition: all 100ms ease;
    background-color: #fff;
    border-radius: 2px;
    z-index: 3001;
    box-shadow: 0 2px 2px 0 rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%), 0 1px 5px 0 rgb(0 0 0 / 20%);
}
.anvil-role-ae-autocomplete.visible-false, .anvil-role-ae-autocomplete.anvil-visible-false {
    transform: scaleX(0) scaleY(0);
    opacity: 0;
    display: block !important;
    transition: all 200ms ease;
}
.anvil-role-ae-autocomplete a {
    padding: 7px 16px;
}
.anvil-role-ae-autocomplete a:hover, .anvil-role-ae-autocomplete a.anvil-role-ae-autocomplete-active {
    background-color: #eee;
}
"""
)


TB = _pluggable_ui["anvil.TextBox"]

# the pluggable ui component might be a callable rather than a class
TB_Class = type(TB())


AUTOCOMPLETE_PROPS = [
    {
        "name": "suggestions",
        "type": "text[]",
        "description": "The list of suggestions to display",
        "default_value": [],
        "group": "autocomplete",
        "important": True,
        "priority": 100,
    },
    {
        "name": "suggest_if_empty",
        "type": "boolean",
        "description": "Whether to suggest suggestions when the text is empty",
        "default_value": True,
        "group": "autocomplete",
        "important": True,
    },
    {
        "name": "filter_mode",
        "type": "enum",
        "description": "How the autocompletion should filter suggestions",
        "options": ["contains", "startswith"],
        "default_value": "contains",
        "group": "autocomplete",
        "important": True,
    },
]

TB_PROPS = TB_Class._anvil_properties_


class Autocomplete(get_design_component(TB_Class)):
    _anvil_properties_ = AUTOCOMPLETE_PROPS + TB_PROPS
    _anvil_events_ = [
        {"name": "suggestion_clicked"},
        {"name": "pressed_enter", "defaultEvent": True},
        {"name": "focus"},
        {"name": "lost_focus"},
        {"name": "change"},
    ]

    def __init__(self, **properties):

        self._active_nodes = []
        self._active = None
        self._active_index = -1
        self._link_height = 0
        self._nodes = {}
        self._filter_mode = None
        self._filter_fn = self._filter_contains

        self._lp = _LinearPanel(
            role="ae-autocomplete",
            spacing_above="none",
            spacing_below="none",
            visible=False,
        )
        self._lp_node = _get_dom_node(self._lp)

        dom_node = self._dom_node = _get_dom_node(self)
        if dom_node.tagName != "INPUT":
            dom_node = self._dom_node = dom_node.querySelector("input")

        tb_props = {
            k: v
            for k, v in properties.items()
            if any(prop["name"] == k for prop in TB_PROPS)
        }
        super().__init__(**tb_props)

        for prop in AUTOCOMPLETE_PROPS:
            setattr(self, prop["name"], properties.get(prop["name"]))

        # use capture for keydown so we can get the event before anvil does
        dom_node.addEventListener("keydown", self._on_keydown, True)
        dom_node.addEventListener("input", self._on_input)
        dom_node.addEventListener("focus", self._on_focus, True)
        dom_node.addEventListener("blur", self._on_blur)
        self.set_event_handler("x-popover-init", self._handle_popover)
        self.set_event_handler("x-popover-destroy", self._handle_popover)
        self.add_event_handler("x-anvil-page-added", self._on_show)
        self.add_event_handler("x-anvil-page-removed", self._on_hide)

        self._virtualizer = Virtualizer(
            count=0,
            estimate_size=lambda idx: 48,
            component=self,
            scroll_element=self._lp_node,
            on_change=self._populate,
        )

    ###### PRIVATE METHODS ######
    @staticmethod
    def _filter_contains(text, search):
        return text.lower().find(search)

    @staticmethod
    def _filter_startswith(text, search):
        return 0 if text.lower().startswith(search) else -1

    def _gen_active_nodes(self):
        prev_active = self._active
        self._reset_autocomplete()

        search_term = self.text.lower()
        if not search_term and not self.suggest_if_empty:
            return

        n = len(search_term)
        filter_fn = self._filter_fn

        def get_node_with_emph(text):
            i = filter_fn(text, search_term)
            if i == -1:
                return False
            node = self._get_node(text)
            if n:
                node.tag.innerHTML = (
                    text[:i] + "<b>" + text[i : i + n] + "</b>" + text[i + n :]
                )
            return node

        self._active_nodes = [
            node for node in map(get_node_with_emph, self.suggestions) if node
        ]
        try:
            self._active_index = self._active_nodes.index(prev_active)
            self._active = prev_active
            self._active.role = "ae-autocomplete-active"
        except ValueError:
            pass

        self._virtualizer.update(count=len(self._active_nodes))

    def _populate(self):
        self._lp.clear()

        self._lp_node.firstElementChild.style.height = (
            f"{self._virtualizer.get_total_size()}px"
        )

        for item in self._virtualizer.get_virtual_items():
            node = self._active_nodes[item.index]
            if node.parent is not None:
                print(f"Warning: you have duplicate suggestions - ignoring {node.text}")
                continue
            self._lp.add_component(node)
            _get_dom_node(node).parentElement.style.top = f"{item.start}px"

        self._lp.visible = bool(self._active_nodes)

    def _get_node(self, text):
        link = self._nodes.get(text)
        if link:
            link.text = link.text
            return link

        link = _Link(text=text, spacing_above="none", spacing_below="none")
        link.set_event_handler("click", self._set_text)
        l_node = _get_dom_node(link)
        link.tag = l_node.querySelector("div")
        # this stops the lost_focus event firing when a suggestion is clicked
        l_node.addEventListener("mousedown", lambda e: e.preventDefault())

        self._nodes[text] = link
        return link

    def _set_text(self, sender=None, *e, **e_args):
        if sender is not None:
            self.text = sender.text
            self._reset_autocomplete()
            self.raise_event("suggestion_clicked")
        elif self._active is not None:
            self.text = self._active.text
            self._reset_autocomplete()
        else:
            self._reset_autocomplete()

    def _reset_autocomplete(self):
        if self._active is not None:
            self._active.role = None
        self._active = None
        self._lp.visible = False
        self._active_nodes = []
        self._active_index = -1
        self._lp_node.scrollTop = 0
        self._virtualizer.update(count=0)

    def _reset_position(self, *e):
        rect = self._dom_node.getBoundingClientRect()
        root_rect = _document.documentElement.getBoundingClientRect()
        body_rect = _document.body.getBoundingClientRect()
        fixed_offset_top = body_rect.top - root_rect.top
        lp_node = self._lp_node
        lp_node.style.left = f"{rect.left - body_rect.left}px"
        lp_node.style.top = f"{rect.bottom - body_rect.top + fixed_offset_top + 5}px"
        lp_node.style.width = f"{rect.width}px"

    ###### INTERNAL EVENTS ######
    def _on_keydown(self, e):
        key = getattr(e, "key", None)
        if key in ("ArrowDown", "ArrowUp"):
            e.preventDefault()
        elif key == "Enter":
            self._set_text()
            return
        elif key == "Escape":
            self._reset_autocomplete()
            return
        else:
            return

        try:
            if key == "ArrowDown":
                i = min(self._active_index + 1, len(self._active_nodes) - 1)
                new_active = self._active_nodes[i]
            else:
                i = max(self._active_index - 1, -1)
                new_active = None if i == -1 else self._active_nodes[i]
        except IndexError:
            return

        self._active_index = i
        if self._active is not None:
            self._active.role = None
        if new_active is not None:
            new_active.role = "ae-autocomplete-active"
            self._virtualizer.scroll_to_index(i)

        self._active = new_active

    def _on_input(self, e):
        """This method is called when the text in this text box is edited"""
        self._gen_active_nodes()
        self._populate()

    def _on_focus(self, e):
        """This method is called when the TextBox gets focus"""
        self._reset_position()
        self._gen_active_nodes()
        self._populate()

    def _on_blur(self, e):
        """This method is called when the TextBox loses focus"""
        self._reset_autocomplete()

    def _on_show(self, **e_args):
        """This method is called when the TextBox is shown on the screen"""
        _document.body.appendChild(self._lp_node)
        _S(_window).on("resize", self._reset_position)

    def _on_hide(self, **e_args):
        """This method is called when the TextBox is removed from the screen"""
        try:
            self._lp_node.remove()
        except Exception:
            pass
        _S(_window).off("resize", self._reset_position)
        self._nodes = {}

    def _handle_popover(self, init_node, **event_args):
        init_node(self._lp_node)

    ##### Properties ######
    @property
    def suggestions(self):
        return self._data or []

    @suggestions.setter
    def suggestions(self, val):
        self._data = val
        if self._dom_node is _document.activeElement:
            self._gen_active_nodes()
            self._populate()

    @property
    def filter_mode(self):
        return self._filter_mode

    @filter_mode.setter
    def filter_mode(self, value):
        self._filter_mode = value
        if value == "startswith":
            self._filter_fn = self._filter_startswith
        else:
            self._filter_fn = self._filter_contains
