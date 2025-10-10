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

__version__ = "3.5.0"

DEFAULT_STYLE = (
    "display: flex; "
    "align-items: var(--ae-cbg-align, center); "
    "gap: var(--ae-cbg-gap, 8px); "
    "flex-direction: var(--ae-cbg-direction, row); "
    "justify-content: var(--ae-cbg-justify, flex-start);"
)
if in_designer:
    DEFAULT_STYLE += "min-height: 40px;"


class CheckBoxGroup(anvil.Container):
    _anvil_events_ = [
        {"name": "change", "defaultEvent": True},
        {"name": "show"},
        {"name": "hide"},
    ]
    _anvil_properties_ = [
        {
            "name": "selected_values",
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
        {"name": "checkboxes", "type": "object"},
    ]
    _id = 0

    def __new__(cls, **properties):
        self = super().__new__(cls)
        id = cls._id
        cls._id += 1
        self._props = {}
        self.css_vars = {}
        self._init = False
        self._name = f"cbg-{id}"
        self._checkboxes = []
        self._dom = crelt(
            "div",
            style=DEFAULT_STYLE,
            role="group",
            ariaOrientation="horizontal",  # default orientation corresponds to row
        )
        self._placeholder = crelt(
            "div", style="font-style: italic; margin: auto; opacity: 0.3;"
        )
        self._placeholder.textContent = "Add CheckBoxes or set .items"
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
        selected_values=None,
        gap=8,
        spacing=None,
        direction=None,
        align=None,
        visible=True,
        checkboxes=None,
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
        if checkboxes is not None:
            self.checkboxes = checkboxes
        # enable style application and compose once
        self._init = True
        self._apply_style()
        self.selected_values = selected_values

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

        if isinstance(c, anvil.CheckBox):
            self._add_checkbox(c)

    def _remove_component(self, c):
        if isinstance(c, anvil.CheckBox):
            self._remove_checkbox(c)

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
    def checkboxes(self):
        return self._checkboxes

    @checkboxes.setter
    def checkboxes(self, v):
        handler = self._handle_checkbox_change

        prev_checkboxes = self._checkboxes
        for cb in prev_checkboxes:
            cb.remove_event_handler("change", handler)

        self._checkboxes = list(v or [])

        for cb in self._checkboxes:
            cb.add_event_handler("change", handler)

    def _add_checkbox(self, cb):
        self._checkboxes.append(cb)
        cb.add_event_handler("change", self._handle_checkbox_change)

    def _remove_checkbox(self, cb):
        self._checkboxes.remove(cb)
        cb.remove_event_handler("change", self._handle_checkbox_change)

    def _handle_checkbox_change(self, **event_args):
        self._handle_change()

    def _handle_change(self):
        self.raise_event("x-anvil-write-back-selected_values")
        self.raise_event("change")

    @property
    def _selected_checkboxes(self):
        return [cb for cb in self._checkboxes if cb.checked]

    @property
    def selected_values(self):
        selected = []
        for checkbox in self._checkboxes:
            if checkbox.checked:
                value = self._item_values.get(checkbox, checkbox.text)
                selected.append(value)
        return selected

    @selected_values.setter
    def selected_values(self, requested_values):
        if requested_values is None:
            requested_values = []

        # Convert to set for efficient lookup
        requested_set = set(requested_values)
        item_values = self._item_values

        for checkbox in self._checkboxes:
            value = item_values.get(checkbox, checkbox.text)
            checkbox.checked = value in requested_set

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
        parts = "".join(f"--ae-cbg-{k}: {v};" for k, v in self.css_vars.items())
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
        checkboxes = []
        selected_values = self.selected_values
        value = value or []

        for i, item in enumerate(value):
            if isinstance(item, str):
                text = real_value = item
            elif isinstance(item, (tuple, list)):
                text, real_value = item
            else:
                raise TypeError(
                    f"item at index {i} is not a str or tuple, got {type(item)}"
                )

            cb = anvil.CheckBox(
                text=text,
                checked=real_value in selected_values,
            )
            item_values[cb] = real_value
            checkboxes.append(cb)

        self.clear()
        for cb in checkboxes:
            self.add_component(cb)
        self._item_values = item_values
