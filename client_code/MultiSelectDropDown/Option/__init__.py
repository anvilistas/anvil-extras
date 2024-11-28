# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil import HtmlPanel as _HtmlPanel
from anvil.js import get_dom_node

from ...utils._component_helpers import _add_roles, _remove_roles
from ._anvil_designer import OptionTemplate

__version__ = "3.1.0"


class Divider(_HtmlPanel):
    _anvil_events_ = ["click"]
    is_divider = True

    def __init__(self):
        get_dom_node(self).dataset["divider"] = ""
        self.key = ""
        self.value = None

    @property
    def selected(self):
        return False

    @selected.setter
    def selected(self, val):
        pass


class Option(OptionTemplate):
    is_divider = False

    def __init__(self, **properties):
        self._props = properties
        self._dom_node = get_dom_node(self)
        self._icon_node = get_dom_node(self.icon_checked)
        self._icon_node.style.visibility = "hidden"
        self.label.role = "ae-ms-option-label"
        self.label_sub.role = "ae-ms-option-subtext"
        self.role = ["ae-ms-option"]

        self.init_components(**properties)
        self._dom_node.addEventListener("focus", self._on_focus)
        self._dom_node.addEventListener("blur", self._on_blur)

    @property
    def selected(self):
        return self._props.get("selected", False)

    @selected.setter
    def selected(self, val):
        if self.disabled:
            return
        self._props["selected"] = val
        self._icon_node.style.visibility = "visible" if val else "hidden"

    @property
    def active(self):
        return "ae-ms-option-active" in self.role

    @active.setter
    def active(self, val):
        if val:
            _add_roles(self, "ae-ms-option-active")
            self._dom_node.scrollIntoView({"block": "nearest"})
        else:
            _remove_roles(self, "ae-ms-option-active")

    @property
    def disabled(self):
        return self._props.get("disabled", False)

    @disabled.setter
    def disabled(self, val):
        self._props["disabled"] = val
        if val:
            self._dom_node.dataset["disabled"] = ""
        else:
            del self._dom_node.dataset["disabled"]

    def focus(self):
        self._dom_node.focus()

    def click(self):
        self.raise_event("click")

    def _on_focus(self, e):
        if not self.disabled:
            self.active = True

    def _on_blur(self, e):
        self.active = False

    def _on_click(self, **event_args):
        self.selected = not self.selected

    def _on_hide(self, **event_args):
        self.active = False

    def _on_show(self, **event_args):
        if self.disabled:
            # and option isn't dynamic so we can do this on the show event and not worry about it
            self._dom_node.parentElement.style.cursor = "not-allowed"

    @classmethod
    def from_str(cls, item: str, idx: str) -> tuple:
        key = value = item
        if item == "---":
            return Divider()
        else:
            return cls(idx=idx, key=key, value=value)

    @classmethod
    def from_tuple(cls, item: tuple, idx: int) -> tuple:
        key, value = item
        if not isinstance(key, str):
            raise TypeError(
                f"expected a tuple of the form str, value in items at idx {idx}"
            )
        return cls(idx=idx, key=key, value=value)

    @classmethod
    def from_dict(cls, item: dict, idx: int) -> tuple:
        sentinel = object()

        # if they only set a key and not a value then use the key as the value
        value = item.get("value", sentinel)
        if value is sentinel:
            value = item.get("key")

        title = item.get("title", "")
        icon = item.get("icon", "")
        subtext = item.get("subtext", "")
        disabled = not item.get("enabled", True)
        key = item.get("key")

        return cls(
            idx=idx,
            key=key,
            value=value,
            icon=icon,
            subtext=subtext,
            title=title,
            disabled=disabled,
        )

    @classmethod
    def from_items(cls, items):
        options = []

        for idx, item in enumerate(items):
            if isinstance(item, str):
                option = cls.from_str(item, idx)
            elif isinstance(item, (tuple, list)):
                option = cls.from_tuple(item, idx)
            elif isinstance(item, dict):
                option = cls.from_dict(item, idx)
            else:
                raise TypeError(f"Invalid item at index {idx} (got type {type(item)})")

            options.append(option)

        return options
