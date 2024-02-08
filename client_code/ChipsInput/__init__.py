# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import HtmlPanel as _HtmlPanel
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import navigator

from ..Chip import Chip
from ..utils._component_helpers import _get_color, _html_injector, _spacing_property
from ._anvil_designer import ChipsInputTemplate

__version__ = "2.5.4"

_primary = _get_color(None)

_html_injector.css(
    """
.anvil-extras-chips-input input {
    box-shadow: none !important;
    border: none !important;
    padding: 7px 0 !important;
    margin-bottom: 0 !important;
    flex: 1;
    min-width: 50px;
}
.anvil-extras-chips-input{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    border-bottom: 1px solid;
    align-items: center;
    padding-bottom: 4px;
}

"""
)

_defaults = {
    "primary_placeholder": "",
    "secondary_placeholder": "",
    "chips": [],
    "visible": True,
    "spacing_above": "small",
    "spacing_below": "small",
}


is_android = "Android" in navigator.userAgent


class ChipsInput(ChipsInputTemplate):
    def __init__(self, **properties):
        self._chips = []
        self._deleting = False
        self._placeholder = self._placeholder_0 = self._placeholder_1 = ""

        input_node = _get_dom_node(self.chip_input)
        input_node.addEventListener("keydown", self._chip_input_key_down)

        dom_node = self._dom_node = _get_dom_node(self)
        dom_node.classList.add("anvil-extras-chips-input")
        dom_node.querySelector(".chips-input-placeholder").remove()
        dom_node.querySelector("script").remove()
        self.temp_chip.remove_from_parent()

        properties = _defaults | properties
        self.init_components(**properties)

    @property
    def primary_placeholder(self):
        return self._placeholder_0

    @primary_placeholder.setter
    def primary_placeholder(self, value):
        self._placeholder_0 = value
        if not len(self._chips):
            self.chip_input.placeholder = value
            self._placeholder = value

    @property
    def secondary_placeholder(self):
        return self._placeholder_1

    @secondary_placeholder.setter
    def secondary_placeholder(self, value):
        self._placeholder_1 = value
        if len(self._chips):
            self.chip_input.placeholder = value
            self._placeholder = value

    @property
    def chips(self):
        # make sure chips is immutable
        return tuple(self._chips)

    @chips.setter
    def chips(self, value):
        value = value or []
        if list(value) == self._chips:
            return
        self._chips = []
        if self.can_add:
            self.clear(slot="chips")
        else:
            self.clear()

        seen = set()
        for chip_text in value:
            if chip_text in seen or not chip_text:
                continue
            chip = Chip(text=chip_text, spacing_above="none", spacing_below="none")
            self.add_component(chip, slot="chips")
            chip.set_event_handler("close_click", self._chip_close_click)
            self._chips.append(chip_text)
            seen.add(chip_text)

        self._reset_placeholder()

    visible = _HtmlPanel.visible
    tag = _HtmlPanel.tag
    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")

    ###### PRIVATE METHODS AND PROPS ######

    @property
    def _last_chip(self):
        """throws an error if we have no chips, when used must be wrapped in try/except"""
        components = self.get_components()
        components.remove(self.chip_input)
        return components[-1]

    def _reset_placeholder(self):
        new_placeholder = self._placeholder_1 if self._chips else self._placeholder_0
        if new_placeholder != self._placeholder:
            self.chip_input.placeholder = self._placeholder = new_placeholder

    def _reset_deleting(self, val):
        try:
            self._deleting = val
            self._set_focus(self._last_chip, val)
        except IndexError:
            pass

    def _chip_input_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        chip_text = self.chip_input.text
        if chip_text and chip_text not in self._chips:
            chip = Chip(text=chip_text, spacing_above="none", spacing_below="none")
            self.add_component(chip, slot="chips")
            chip.set_event_handler("close_click", self._chip_close_click)
            self._chips.append(chip_text)
            self.chip_input.text = ""
            self._reset_placeholder()

            self.raise_event("chips_changed")
            self.raise_event("chip_added", chip=chip_text)

    def _chip_input_key_down(self, js_event):
        """This method is called when on the user key down in this text box"""
        try:
            if not self.chip_input.text and js_event.key == "Backspace":
                if not self._deleting:
                    self._reset_deleting(True)
                    return
                _last_chip = self._last_chip
                self._chips.pop()
                chip_text = _last_chip.text
                _last_chip.remove_from_parent()
                self._reset_placeholder()

                self.raise_event("chips_changed")
                self.raise_event("chip_removed", chip=chip_text)

                self._set_focus(self._last_chip, True)

            elif self._deleting:
                self._reset_deleting(False)
                if js_event.key == "Tab":
                    js_event.preventDefault()

            elif is_android and js_event.key == "Tab":
                js_event.preventDefault()
                self._chip_input_pressed_enter()

        except IndexError:
            pass

    def _chip_input_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self._dom_node.style.borderBottom = f"1px solid {_primary}"

    def _chip_input_lost_focus(self, **event_args):
        """This method is called when the TextBox loses focus"""
        self._dom_node.style.borderBottom = "1px solid"
        self._reset_deleting(False)

    def _chip_close_click(self, sender, **event_args):
        chips = self._chips
        chip_text = sender.text
        chips.remove(chip_text)
        sender.remove_from_parent()
        self.raise_event("chips_changed")
        self.raise_event("chip_removed", chip=chip_text)

    @staticmethod
    def _set_focus(chip, val):
        chip.background = _primary if val else ""
        chip.chip_label.foreground = "#fff" if val else ""
        chip.close_link.foreground = "#fff" if val else ""
