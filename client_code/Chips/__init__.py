# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import FlowPanel as _FlowPanel
from anvil import Label as _Label
from anvil import Link as _Link
from anvil.js import get_dom_node as _get_dom_node

from ..session import style_injector as _style_injector
from ..utils._component_helpers import _get_color
from ._anvil_designer import ChipsTemplate

__version__ = "1.3.1"

_primary = _get_color(None)

_style_injector.inject(
    """
.anvil-extras-chips-input .badge {
    font-weight: inherit;
    background-color: #e4e4e4;
    color: inherit;
    border-radius: 14px;
    font-size: inherit;
}
.anvil-extras-chips input {
    box-shadow: none !important;
    padding: 8px 0 4px;
}
.anvil-extras-chips.flow-panel.flow-spacing-small > .flow-panel-gutter { margin: 0 -4px; }
.anvil-extras-chips.flow-panel.flow-spacing-small > .flow-panel-gutter > .flow-panel-item {
  margin-left: 4px;
  margin-right: 4px;
}
.anvil-extras-chips .flow-panel.flow-spacing-small > .flow-panel-gutter { margin: 0 -2px; }
.anvil-extras-chips .flow-panel.flow-spacing-small > .flow-panel-gutter > .flow-panel-item {
  margin-left: 6px;
  margin-right: 6px;
}
"""
)


class Chips(ChipsTemplate):
    def __init__(self, **properties):
        self._chips = []
        self._deleting = False

        input_node = _get_dom_node(self.chip_input)
        input_node.addEventListener("keydown", self._chip_input_key_down)
        # prevent annoying vertical jump of components
        input_node.style.border = "0"
        input_node.style.paddingBottom = "4px"
        input_node.style.paddingTop = "13px"
        input_node.style.marginBottom = "7px"
        input_node.parentNode.style.flex = "1"

        self._dom_node = _get_dom_node(self)
        self._dom_node.classList.add("anvil-extras-chips-input")

        gutter = self._dom_node.firstElementChild
        gutter.style.borderBottom = "1px solid"
        gutter.style.alignItems = "center"
        self._gutter = gutter

        self.init_components(**properties)

    def _chip_input_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        chip_text = self.chip_input.text
        if chip_text and chip_text not in self._chips:
            self.add_component(Chip(chip_text=chip_text), index=len(self._chips))
            self._chips.append(chip_text)
            self.chip_input.text = ""
            self.raise_event("chips_changed")
            self.raise_event("chip_added", chip=chip_text)

    @property
    def placeholder(self):
        return self.chip_input.placeholder

    @placeholder.setter
    def placeholder(self, value):
        self.chip_input.placeholder = value

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
        for component in self.get_components()[:-1]:
            component.remove_parent()
        seen = set()
        for i, chip in enumerate(value):
            if chip in seen or not chip:
                continue
            self.add_component(Chip(chip_text=chip), index=i)
            self._chips.append(chip)
            seen.add(chip)

    visible = _FlowPanel.visible
    spacing_above = _FlowPanel.spacing_above
    spacing_below = _FlowPanel.spacing_below

    @property
    def _last_chip(self):
        return self.get_components()[-2]

    def _reset_deleting(self, val):
        try:
            self._deleting = val
            self._last_chip.is_focused = val
        except IndexError:
            pass

    def _chip_input_key_down(self, js_event):
        """This method is called when the user presses Enter in this text box"""
        try:
            if not self.chip_input.text and js_event.key == "Backspace":
                if not self._deleting:
                    self._reset_deleting(True)
                    return
                _last_chip = self._last_chip
                self._chips.pop()
                chip_text = _last_chip.chip_text
                _last_chip.remove_from_parent()
                self.raise_event("chips_changed")
                self.raise_event("chip_removed", chip=chip_text)
                self._last_chip.is_focused = True
            elif self._deleting:
                self._reset_deleting(False)
                if js_event.key == "Tab":
                    js_event.preventDefault()
        except IndexError:
            pass

    def _chip_input_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self._gutter.style.borderBottom = f"1px solid {_primary}"

    def _chip_input_lost_focus(self, **event_args):
        """This method is called when the TextBox loses focus"""
        self._gutter.style.borderBottom = "1px solid"
        self._reset_deleting(False)


class Chip(_FlowPanel):
    def __init__(self, chip_text="", **properties):
        self.chip_label = _Label(
            text=chip_text, spacing_above="none", spacing_below="none"
        )
        self.chip_close = _Link(
            text="\u2715", spacing_above="none", spacing_below="none"
        )
        self.chip_close.set_event_handler("click", self.chip_close_click)
        self.add_component(self.chip_label)
        self.add_component(self.chip_close)
        self.is_focused = False
        self.chip_text = chip_text
        _dom_node = _get_dom_node(self)
        _dom_node.classList.add("badge")
        super().__init__(**properties, spacing="small")

    @property
    def is_focused(self):
        return self._focused

    @is_focused.setter
    def is_focused(self, val):
        self._focused = val
        self.background = _primary if val else ""
        self.chip_label.foreground = "#fff" if val else ""
        self.chip_close.foreground = "#fff" if val else ""

    def chip_close_click(self, **event_args):
        chips = self.parent._chips
        parent = self.parent
        chip_text = self.chip_text
        chips.remove(chip_text)
        self.remove_from_parent()
        parent.raise_event("chips_changed")
        parent.raise_event("chip_removed", chip=chip_text)
