# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import partial

import anvil
from anvil.designer import in_designer
from anvil.property_utils import (
    get_unset_spacing,
    set_element_spacing,
    set_element_visibility,
)

from .utils._component_helpers import _css_length, crelt

__version__ = "3.2.0"

DEFAULT_STYLE = (
    "display: flex; "
    "align-items: var(--ae-rg-align, center); "
    "gap: var(--ae-rg-gap, 8px); "
    "flex-direction: var(--ae-rg-direction, row); "
    "justify-content: var(--ae-rg-justify, flex-start);"
)
if in_designer:
    DEFAULT_STYLE += "min-height: 40px;"


class RadioGroup(anvil.Container):
    _anvil_events_ = [
        {"name": "change", "defaultEvent": True},
        {"name": "show"},
        {"name": "hide"},
    ]
    _anvil_properties_ = [
        {
            "name": "selected_value",
            "type": "object",  # set at runtime
            "supportsWriteback": True,
            "important": True,
            "priority": 10,
        },
        {"name": "gap", "type": "string", "group": "layout", "important": True},
        {"name": "spacing", "type": "spacing", "group": "spacing"},
        {
            "name": "direction",
            "type": "enum",
            "options": ["horizontal", "vertical"],
            "includeNoneOption": True,
            "group": "layout",
        },
        {
            "name": "align",
            "type": "enum",
            "options": [
                "left",
                "center",
                "right",
                "space-evenly",
                "space-between",
                "space-around",
            ],
            "includeNoneOption": True,
            "designerHint": "align-horizontal",
            "group": "layout",
            "important": True,
        },
        {
            "name": "visible",
            "type": "boolean",
            "designerHint": "visible",
            "group": "appearance",
        },
        {"name": "items", "type": "text[]", "important": True},
        {"name": "class_name", "type": "string", "group": "style"},
        {"name": "style", "type": "string", "group": "style"},
        {"name": "buttons", "type": "object"},
    ]
    _id = 0

    def __new__(cls, **properties):
        self = super().__new__(cls)
        id = cls._id
        cls._id += 1
        self._props = {}
        self.css_vars = {}
        self._init = False
        self._name = f"rg-{id}"
        self._buttons = []
        self._dom = crelt(
            "div",
            style=DEFAULT_STYLE,
            role="radiogroup",
            ariaOrientation="horizontal",  # default orientation corresponds to row
        )
        self._placeholder = crelt(
            "div", style="font-style: italic; margin: auto; opacity: 0.3;"
        )
        self._placeholder.textContent = "Add RadioButtons or set .items"
        self._dropzones = []
        self._item_values = {}

        if in_designer:
            self._dom.append(self._placeholder)

        self.add_event_handler(
            "x-anvil-classic-show", lambda **e: self.raise_event("show")
        )
        self.add_event_handler(
            "x-anvil-classic-hide", lambda **e: self.raise_event("hide")
        )

        return self

    def __init__(
        self,
        items=None,
        selected_value=None,
        gap=8,
        spacing=None,
        direction=None,
        align=None,
        visible=True,
        buttons=None,
        class_name=None,
        style=None,
        **properties,
    ):
        super().__init__()
        self.gap = gap
        self.spacing = spacing
        self.direction = direction
        self.align = align
        self.items = items
        self.visible = visible
        self.class_name = class_name
        self.style = style
        if buttons is not None:
            self.buttons = buttons
        # enable style application and compose once
        self._init = True
        self._apply_style()
        self.selected_value = selected_value

    def add_component(self, c, index=None, **layout_props):
        self._placeholder.remove()

        super().add_component(
            c, index=index, on_remove=partial(self._remove_component, c)
        )

        real_index = self.get_components().index(c)
        child = self._dom.children.get(real_index)
        dom_node = c._anvil_setup_dom_()
        # wrapper is purely presentational and fixes a bootstrap annoying style issue
        wrapper = crelt("div", role="none")
        wrapper.append(dom_node)
        if child:
            self._dom.insertBefore(wrapper, child)
        else:
            self._dom.appendChild(wrapper)

        if isinstance(c, anvil.RadioButton):
            self._add_button(c)

    def _remove_component(self, c):
        if isinstance(c, anvil.RadioButton):
            self._remove_button(c)

        # remove the wrapper we added in add_component (if present)
        el = c._anvil_dom_element_
        wrapper = el.parentNode
        if wrapper is not None:
            wrapper.remove()

        if in_designer and not self.get_components():
            self._dom.append(self._placeholder)

    def _anvil_get_unset_property_values_(self):
        dom = self._dom
        sp = get_unset_spacing(dom, dom, self.spacing)
        return {"spacing": sp}

    def _gen_drop_zone(self):
        el = crelt("div")
        index = len(self._dropzones)
        dz = {
            "element": el,
            "dropInfo": {
                "minChildIdx": index,
                "maxChildIdx": index,
            },
        }
        self._dropzones.append(dz)
        return dz

    def _anvil_enable_drop_mode_(self, *args):
        self._anvil_disable_drop_mode_()
        self._placeholder.remove()

        children = list(self._dom.children)
        for c in children:
            dz = self._gen_drop_zone()
            c.insertAdjacentElement("beforebegin", dz["element"])

        dz = self._gen_drop_zone()
        self._dom.insertAdjacentElement("beforeend", dz["element"])

        return self._dropzones

    def _anvil_disable_drop_mode_(self):
        for dz in self._dropzones:
            dz["element"].remove()

        self._dropzones = []
        if not self.get_components():
            self._dom.append(self._placeholder)

    def _anvil_setup_dom_(self):
        return self._dom

    @property
    def _anvil_dom_element_(self):
        return self._dom

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, v):
        handler = self._handle_button_change

        prev_buttons = self._buttons
        for b in prev_buttons:
            b.remove_event_handler("change", handler)
            b.group_name = None

        self._buttons = list(v or [])

        for b in self._buttons:
            b.add_event_handler("change", handler)
            b.group_name = self._name

    def _add_button(self, b):
        self._buttons.append(b)
        b.add_event_handler("change", self._handle_button_change)
        b.group_name = self._name

    def _remove_button(self, b):
        self._buttons.remove(b)
        b.remove_event_handler("change", self._handle_button_change)
        b.group_name = None
        if self._selected_button is b:
            self._selected_button = None

    def _handle_button_change(self, **event_args):
        self._handle_change()

    def _handle_change(self):
        self.raise_event("x-anvil-write-back-selected_value")
        self.raise_event("change")

    @property
    def _selected_button(self):
        for button in self._buttons:
            if button.selected:
                return button
        return None

    @_selected_button.setter
    def _selected_button(self, button):
        if button is None:
            # Deselect the currently selected button
            _selected_button = self._selected_button
            if _selected_button:
                _selected_button.selected = False
        else:
            if button not in self._buttons:
                raise ValueError("RadioButton is not in this group")
            button.selected = True

    @property
    def selected_value(self):
        button = self._selected_button
        if button is None:
            return None
        else:
            return self._item_values.get(button, button.value)

    @selected_value.setter
    def selected_value(self, requested_value):
        item_values = self._item_values
        for button in self._buttons:
            if item_values.get(button, button.value) == requested_value:
                self._selected_button = button
                return
        self._selected_button = None

    @property
    def gap(self):
        return self._props.get("gap")

    @gap.setter
    def gap(self, value):
        self._props["gap"] = value
        self.css_vars["gap"] = _css_length(value)
        self._apply_style()

    @property
    def direction(self):
        return self._props.get("direction")

    @direction.setter
    def direction(self, value):
        self._props["direction"] = value
        dir_val = "column" if value == "vertical" else "row"
        self.css_vars["direction"] = dir_val
        if value == "vertical":
            self._dom.setAttribute("aria-orientation", "vertical")
        else:
            self._dom.setAttribute("aria-orientation", "horizontal")

        self._set_align_vars()
        self._apply_style()

    @property
    def spacing(self):
        return self._props.get("spacing")

    @spacing.setter
    def spacing(self, value):
        self._props["spacing"] = value
        set_element_spacing(self._dom, value)

    @property
    def visible(self):
        return self._props.get("visible")

    @visible.setter
    def visible(self, value):
        self._props["visible"] = value
        set_element_visibility(self._dom, value)
        # reflect visibility state for assistive tech
        self._dom.setAttribute("aria-hidden", "false" if value else "true")

    def _apply_style(self):
        """Compose inline style as: VARS + DEFAULT_STYLE + user style."""
        # Skip during construction to avoid repeated recomposition
        if not self._init:
            return
        parts = "".join(f"--ae-rg-{k}: {v};" for k, v in self.css_vars.items())
        user_style = self._props.get("style") or ""
        composed = parts + " " + DEFAULT_STYLE + " " + user_style
        self._dom.setAttribute("style", composed)
        # Re-apply spacing after resetting inline style so margins persist
        sp = self._props.get("spacing")
        if sp is not None:
            set_element_spacing(self._dom, sp)

    def _set_align_vars(self):
        """Derive --align/--justify based on current align and direction."""
        align_val = self._props.get("align")
        # Clear to defaults when unset
        if not align_val:
            self.css_vars.pop("align", None)
            self.css_vars.pop("justify", None)
            return
        if align_val == "left":
            css = "flex-start"
        elif align_val == "right":
            css = "flex-end"
        else:
            css = align_val
        dir_val = self.css_vars.get("direction") or (
            "column" if self._props.get("direction") == "vertical" else "row"
        )
        if dir_val == "column":
            self.css_vars["align"] = css
            self.css_vars.pop("justify", None)
        else:
            self.css_vars["justify"] = css
            self.css_vars.pop("align", None)

    @property
    def class_name(self):
        return self._props.get("class_name")

    @class_name.setter
    def class_name(self, value):
        self._props["class_name"] = value
        self._dom.className = value or ""

    @property
    def style(self):
        return self._props.get("style")

    @style.setter
    def style(self, value):
        self._props["style"] = value or ""
        self._apply_style()

    @property
    def align(self):
        return self._props.get("align")

    @align.setter
    def align(self, value):
        self._props["align"] = value
        self._set_align_vars()
        self._apply_style()

    @property
    def items(self):
        return self._props.get("items")

    @items.setter
    def items(self, value):
        self._props["items"] = value
        item_values = {}
        buttons = []
        selected_value = self.selected_value
        value = value or []

        for i, item in enumerate(value):
            if isinstance(item, str):
                text = value = real_value = item
            elif isinstance(item, (tuple, list)):
                text, real_value = item
                value = str(i)
            else:
                raise TypeError(
                    f"item at index {i} is not a str or tuple, got {type(item)}"
                )

            b = anvil.RadioButton(
                text=text,
                value=value,
                selected=selected_value == real_value,
            )
            item_values[b] = real_value
            buttons.append(b)

        self.clear()
        for b in buttons:
            self.add_component(b)
        self._item_values = item_values
