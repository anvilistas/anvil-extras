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
from ._anvil_designer import TagsTemplate

__version__ = "1.3.1"

_primary = _get_color(None)

_style_injector.inject(
    """
.anvil-extras-tags .badge {
    font-weight: inherit;
    background-color: #e4e4e4;
    color: inherit;
    border-radius: 14px;
    font-size: inherit;
}
.anvil-extras-tags input {
    box-shadow: none !important;
    padding: 8px 0 4px;
}
.anvil-extras-tags.flow-panel.flow-spacing-small > .flow-panel-gutter { margin: 0 -4px; }
.anvil-extras-tags.flow-panel.flow-spacing-small > .flow-panel-gutter > .flow-panel-item {
  margin-left: 4px;
  margin-right: 4px;
}
.anvil-extras-tags .flow-panel.flow-spacing-small > .flow-panel-gutter { margin: 0 -2px; }
.anvil-extras-tags .flow-panel.flow-spacing-small > .flow-panel-gutter > .flow-panel-item {
  margin-left: 6px;
  margin-right: 6px;
}
"""
)


class Tags(TagsTemplate):
    def __init__(self, **properties):
        self._tags = []
        self._deleting = False

        input_node = _get_dom_node(self.tag_input)
        input_node.addEventListener("keydown", self._tag_input_key_down)
        # prevent annoying vertical jump of components
        input_node.style.border = "0"
        input_node.style.paddingBottom = "4px"
        input_node.style.paddingTop = "13px"
        input_node.style.marginBottom = "7px"
        input_node.parentNode.style.flex = "1"

        self._dom_node = _get_dom_node(self)
        self._dom_node.classList.add("anvil-extras-tags")

        gutter = self._dom_node.firstElementChild
        gutter.style.borderBottom = "1px solid"
        gutter.style.alignItems = "center"
        self._gutter = gutter

        self.init_components(**properties)

    def _tag_input_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        tag_text = self.tag_input.text
        if tag_text and tag_text not in self._tags:
            self.add_component(Tag(tag_text=tag_text), index=len(self._tags))
            self._tags.append(tag_text)
            self.tag_input.text = ""
            self.raise_event("tags_changed")
            self.raise_event("tag_added", tag=tag_text)

    @property
    def placeholder(self):
        return self.tag_input.placeholder

    @placeholder.setter
    def placeholder(self, value):
        self.tag_input.placeholder = value

    @property
    def tags(self):
        # make sure tags is immutable
        return tuple(self._tags)

    @tags.setter
    def tags(self, value):
        value = value or []
        if list(value) == self._tags:
            return
        self._tags = []
        for component in self.get_components()[:-1]:
            component.remove_parent()
        seen = set()
        for i, tag in enumerate(value):
            if tag in seen or not tag:
                continue
            self.add_component(Tag(tag_text=tag), index=i)
            self._tags.append(tag)
            seen.add(tag)

    visible = _FlowPanel.visible
    spacing_above = _FlowPanel.spacing_above
    spacing_below = _FlowPanel.spacing_below

    @property
    def _last_tag(self):
        return self.get_components()[-2]

    def _reset_deleting(self, val):
        try:
            self._deleting = val
            self._last_tag.is_focused = val
        except IndexError:
            pass

    def _tag_input_key_down(self, js_event):
        """This method is called when the user presses Enter in this text box"""
        try:
            if not self.tag_input.text and js_event.key == "Backspace":
                if not self._deleting:
                    self._reset_deleting(True)
                    return
                _last_tag = self._last_tag
                self._tags.pop()
                tag_text = _last_tag.tag_text
                _last_tag.remove_from_parent()
                self.raise_event("tags_changed")
                self.raise_event("tag_removed", tag=tag_text)
                self._last_tag.is_focused = True
            elif self._deleting:
                self._reset_deleting(False)
                if js_event.key == "Tab":
                    js_event.preventDefault()
        except IndexError:
            pass

    def _tag_input_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self._gutter.style.borderBottom = f"1px solid {_primary}"

    def _tag_input_lost_focus(self, **event_args):
        """This method is called when the TextBox loses focus"""
        self._gutter.style.borderBottom = "1px solid"
        self._reset_deleting(False)


class Tag(_FlowPanel):
    def __init__(self, tag_text="", **properties):
        self.tag_label = _Label(
            text=tag_text, spacing_above="none", spacing_below="none"
        )
        self.tag_close = _Link(
            text="\u2715", spacing_above="none", spacing_below="none"
        )
        self.tag_close.set_event_handler("click", self.tag_close_click)
        self.add_component(self.tag_label)
        self.add_component(self.tag_close)
        self.is_focused = False
        self.tag_text = tag_text
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
        self.tag_label.foreground = "#fff" if val else ""
        self.tag_close.foreground = "#fff" if val else ""

    def tag_close_click(self, **event_args):
        tags = self.parent._tags
        parent = self.parent
        tag_text = self.tag_text
        tags.remove(tag_text)
        self.remove_from_parent()
        parent.raise_event("tags_changed")
        parent.raise_event("tag_removed", tag=tag_text)
