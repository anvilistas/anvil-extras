# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import LinearPanel as _LinearPanel
from anvil import Link as _Link
from anvil import TextBox as _TextBox
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S
from anvil.js.window import window as _window

from ..utils._component_helpers import _html_injector
from ._anvil_designer import AutocompleteTemplate

__version__ = "2.2.3"


_html_injector.css(
    """
.anvil-role-autocomplete {
    padding: 0 !important;
}
.anvil-role-autocomplete {
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
.anvil-role-autocomplete.visible-false {
    transform: scaleX(0) scaleY(0);
    opacity: 0;
    display: block !important;
    transition: all 200ms ease;
}
.anvil-role-autocomplete a {
    padding: 7px 16px;
}
.anvil-role-autocomplete a:hover, .anvil-role-autocomplete a.anvil-role-active {
    background-color: #eee;
}
"""
)


class Autocomplete(AutocompleteTemplate):
    def __init__(self, **properties):
        self._active_nodes = []
        self._active = None
        self._active_index = -1
        self._link_height = 0
        self._nodes = {}

        self.init_components(**properties)

        self._lp = _LinearPanel(
            role="autocomplete",
            spacing_above="none",
            spacing_below="none",
            visible=False,
        )
        self._lp_node = _get_dom_node(self._lp)

        dom_node = self._dom_node = _get_dom_node(self)
        # use capture for keydown so we can get the event before anvil does
        dom_node.addEventListener("keydown", self._on_keydown, True)
        dom_node.addEventListener("input", self._on_input)
        dom_node.addEventListener("focus", self._on_focus, True)
        dom_node.addEventListener("blur", self._on_blur)
        self.set_event_handler("x-popover-init", self._mk_popover)

        # ensure the same method is passed to $(window).off('resize')
        self._reset_position = self._reset_position

    ###### PRIVATE METHODS ######
    def _populate(self):
        prev_active = self._active
        self._reset_autocomplete()
        self._lp.clear()

        search_term = self.text.lower()
        if not search_term and not self.suggest_if_empty:
            return

        n = len(search_term)

        def get_node_with_emph(text):
            i = text.lower().find(search_term)
            if i == -1:
                return False
            node = self._get_node(text)
            if n:
                node.tag.innerHTML = (
                    text[:i] + "<b>" + text[i : i + n] + "</b>" + text[i + n :]
                )
            return node

        nodes = filter(None, map(get_node_with_emph, self.suggestions))
        for node in nodes:
            if node.parent is not None:
                print(f"Warning: you have duplicate suggestions - ignoring {node.text}")
                continue
            self._lp.add_component(node)
            self._active_nodes.append(node)

        self._lp.visible = bool(self._active_nodes)
        try:
            self._active_index = self._active_nodes.index(prev_active)
            self._active = prev_active
            self._active.role = "active"
        except ValueError:
            pass

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

    def _reset_autocomplete(self):
        if self._active is not None:
            self._active.role = None
        self._active = None
        self._lp.visible = False
        self._active_nodes = []
        self._active_index = -1
        self._lp_node.scrollTop = 0

    def _reset_position(self, *e):
        box = self._dom_node.getBoundingClientRect()
        body = _document.body.getBoundingClientRect()
        lp_node = self._lp_node
        lp_node.style.left = f"{box.left - body.left}px"
        lp_node.style.top = f"{box.bottom - body.top + 5}px"
        lp_node.style.width = f"{box.width}px"

    ###### INTERNAL EVENTS ######
    def _on_keydown(self, e):
        key = getattr(e, "key", None)
        if key in ("ArrowDown", "ArrowUp"):
            e.preventDefault()
        elif key == "Enter":
            self._set_text()
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
            new_active.role = "active"
            self._link_height = (
                self._link_height or _get_dom_node(new_active).clientHeight
            )
            self._lp_node.scrollTop = max(0, self._link_height * (i - 4))

        self._active = new_active

    def _on_input(self, e):
        """This method is called when the text in this text box is edited"""
        self._populate()

    def _on_focus(self, e):
        """This method is called when the TextBox gets focus"""
        self._reset_position()
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
        self._lp_node.remove()
        _S(_window).off("resize", self._reset_position)

    def _mk_popover(self, init_node, **event_args):
        init_node(self._lp_node)

    ##### Properties ######
    @property
    def suggestions(self):
        return self._data or []

    @suggestions.setter
    def suggestions(self, val):
        self._data = val

    text = _TextBox.text
    placeholder = _TextBox.placeholder
    spacing_above = _TextBox.spacing_above
    spacing_below = _TextBox.spacing_below
    enabled = _TextBox.enabled
    foreground = _TextBox.foreground
    background = _TextBox.background
    visible = _TextBox.visible
    tag = _TextBox.tag
