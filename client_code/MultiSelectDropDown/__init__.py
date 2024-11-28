# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil.js as _js
from anvil import HtmlPanel as _HtmlPanel
from anvil.js.window import document as _document

from ..popover import pop, popover
from ..utils._component_helpers import _css_length, _html_injector, _spacing_property
from ._anvil_designer import MultiSelectDropDownTemplate
from .DropDown import DropDown
from .Option import Option

__version__ = "3.1.0"

_css = """
.anvil-role-ae-ms-btn > button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.anvil-role-ae-ms-btn > button > span {
    text-overflow: ellipsis;
    white-space: nowrap !important;
    overflow: hidden;
}

/* dropdown */
.ae-ms-dd {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.ae-ms-select-all button > span {
    text-wrap: nowrap !important;
}

.ae-ms-options {
    min-height: 0;
}

.ae-ms-options:focus-visible {
    outline: none;
}
.ae-ms-options > div {
    height: 100%
}
.ae-ms-options ul {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: scroll;
}

.ae-ms-options a[data-disabled] {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}
.ae-ms-options a[data-disabled] * {
    pointer-events: none;
}

.ae-ms-options div[data-divider] {
    height: 1px;
    margin: 9px 0;
    overflow: hidden;
    background-color: #e5e5e5;
}

.ae-ms-options .anvil-panel-section-gutter,
.ae-ms-options .flow-panel-gutter,
.ae-ms-options .anvil-flow-panel-gutter,
.ae-ms-options .anvil-panel-col,
.ae-ms-options .flow-panel-item,
.ae-ms-options .anvil-flow-panel-item {
    margin: 0 !important;
}
.ae-ms-options .anvil-panel-col,
.ae-ms-options .flow-panel-item,
.ae-ms-options .anvil-flow-panel-item {
    padding: 0 !important;
}
.ae-ms-options .flow-panel-gutter,
.ae-ms-options .anvil-flow-panel-gutter {
    gap: 8px;
}

.ae-ms-options a.anvil-role-ae-ms-option {
    color: var(--ae-ms-option-text, #333333);
    padding: 2px 0;
}

.ae-ms-options a.anvil-role-ae-ms-option:hover:not(.anvil-role-ae-ms-option-active) {
    background-color: var(--ae-ms-option-bg-hover, #e8e8e8);
}

.ae-ms-options a.anvil-role-ae-ms-option-active {
    background-color: var(--ae-ms-option-bg-active, #337ab7);
    color: var(--ae-ms-option-text-active, #fff);
}

.anvil-role-ae-ms-option-label span {
    white-space: nowrap !important;
    padding: 0 !important;
}

.anvil-role-ae-ms-option-subtext span {
    white-space: nowrap !important;
    font-size: 80%;
    padding: 0 !important;
    color: var(--ae-ms-option-subtext, #777);
}
.anvil-role-ae-ms-option-active .anvil-role-ae-ms-option-subtext span {
    color: var(--ae-ms-option-subtext-active, rgba(255,255,255,.5));
}

"""
_html_injector.css(_css)

# TODO
# - [x] add support for dividers
# - [x] add support for icons
# - [x] add support for subtext
# - [x] add support for title
# - [x] add support for disabled
# - [x] make the dropwdown conatiner a compnent in it's own right - might even be a custom component
# - [x] add support for select all buttons
#       - [x] we probably need to wrap the lp in a container and add the button to that
#       - [x] only works in multiple mode
# - [x] add arrow key support
#       - [x] active role
#       - [x] when filtering is enabled - ensure the arrow keys work
#         - needs a different approach - can't just do the focus thing
# - [x] add tab key support
# - [x] Consider whether we need the underlying select and options (probably not)
#       - No
# - [x] search box support
#       - [x] focus the search box when the search box is added to the page
# - [x] ensure visible works as expected - i.e. the popover should be hidden when we're not visible
# - [x] support single select dropdown
#       - when an option is selected all other options are hidden
#       - This might be why it's useful to use the underlying option component, because then the browser is responsible for this logic
# - [x] support the various width options
#       - [ ] fit needs to also change the width of the dd to the max
# - [x] support the selected text option
# - [x] support the placeholder text
# - [x] styling and roles
# - [ ] go through each property and make sure it's working as expected
# - [ ] test multi select inside a popover
# - [ ] stop the focus within when enable fitler is false and we hit an arrow key

_defaults = {
    "align": "left",
    "placeholder": "None Selected",
    "enable_filtering": False,
    "multiple": True,
    "enabled": True,
    "items": None,
    "spacing_below": "small",
    "spacing_above": "small",
    "enable_select_all": False,
    "width": "",
    "visible": True,
}


def _props_property(prop, setter):
    def getprop(self):
        return self._props[prop]

    def setprop(self, val):
        self._props[prop] = val
        setter(self, val)

    return property(getprop, setprop, None, prop)


class MultiSelectDropDown(MultiSelectDropDownTemplate):
    def __init__(self, **properties):
        self._init = False
        self._dom_node = _js.get_dom_node(self)
        self._invalid = []
        self._options = []
        self._total = 0
        self._props = props = _defaults | properties
        props["items"] = props["items"] or []

        self._dd_width = 0
        self._dd = DropDown()
        self._dd.add_event_handler("change", self._change)
        popover(
            self._select_btn,
            self._dd,
            placement="bottom-start",
            arrow=False,
            delay=0,
            animation=False,
            trigger="manual",
            max_width="fit-content",
        )

        selected = props.pop("selected", ())

        self.init_components(**props)
        self.set_event_handler("x-popover-init", self._mk_popover)
        self.set_event_handler("x-popover-destroy", self._mk_popover)
        self._dd.set_event_handler(
            "x-popover-show", lambda **e: self.raise_event("opened")
        )
        self._dd.set_event_handler(
            "x-popover-hide", lambda **e: self.raise_event("closed")
        )

        self._init = True
        self.selected = selected

    def format_selected_text(self, count, total):
        if count > 3:
            return f"{count} items selected"
        return ", ".join(opt.title or opt.key for opt in self._options if opt.selected)

    ##### PROPERTIES #####
    @property
    def width(self):
        return self._props.get("width")

    @width.setter
    def width(self, val):
        self._props["width"] = val
        self._dd._dom_node.style.minWidth = ""

        if val == "auto":
            self._select_btn.width = self._dd_width
        elif val == "fit":
            self._select_btn.width = "fit-content"
            self._dd._dom_node.style.minWidth = ""
        elif not val:
            self._select_btn.width = 220
            self._dd._dom_node.style.minWidth = "192px"
        else:
            self._select_btn.width = val
            self._dd._dom_node.style.minWidth = _css_length(val)
        # We might want to change this
        # but if we do we need the btn to be on the screen to calculate the width
        # and we'd probably need to have a resize observer to change the width of the _dd element

    @property
    def align(self):
        return self._select_btn.align

    @align.setter
    def align(self, val):
        self._select_btn.align = val

    @property
    def items(self):
        return self._props["items"]

    @items.setter
    def items(self, value):
        self._props["items"] = value
        self._close()
        selected = self.selected + self._invalid

        options = Option.from_items(value)

        self._dd.options = self._options = options
        self._calc_dd_width()
        self._total = sum(1 for opt in options if not opt.is_divider)
        self.selected = selected
        if self._init:
            self.width = self.width

    @property
    def selected_keys(self):
        return [opt.key for opt in self._options if opt.selected]

    @property
    def selected(self):
        return [opt.value for opt in self._options if opt.selected]

    @selected.setter
    def selected(self, values):
        if not self._init:
            return

        FOUND = object()

        if not isinstance(values, (list, tuple)):
            values = [values]
        else:
            values = list(values)

        multiple = self.multiple
        first = True

        for opt in self._options:
            try:
                idx = values.index(opt.value)
            except ValueError:
                opt.selected = False
            else:
                values[idx] = FOUND
                opt.selected = True if multiple else first
                first = False

        self._invalid = [val for val in values if val is not FOUND]
        self._change(raise_event=False)

    @property
    def placeholder(self):
        return self._props.get("placeholder", "")

    @placeholder.setter
    def placeholder(self, val):
        self._props["placeholder"] = val
        if not self.selected_keys:
            self._select_btn.text = val

    @property
    def enabled(self):
        return self._select_btn.enabled

    @enabled.setter
    def enabled(self, val):
        self._select_btn.enabled = val
        if not val:
            self._close()

    @property
    def enable_filtering(self):
        return self._dd.enable_filtering

    @enable_filtering.setter
    def enable_filtering(self, val):
        self._dd.enable_filtering = val

    @property
    def multiple(self):
        return self._dd.multiple

    @multiple.setter
    def multiple(self, val):
        self._dd.multiple = val
        self.selected = self.selected

    @property
    def enable_select_all(self):
        return self._dd.enable_select_all

    @enable_select_all.setter
    def enable_select_all(self, val):
        self._dd.enable_select_all = val

    tag = _HtmlPanel.tag
    visible = _HtmlPanel.visible
    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")

    ##### PRIVATE Functions #####

    def _calc_dd_width(self):
        dd_node = self._dd._dom_node
        width = dd_node.style.width
        min_width = dd_node.style.minWidth
        dd_node.style.width = "fit-content"
        _document.body.appendChild(dd_node)
        self._dd_width = dd_node.offsetWidth + 28
        dd_node.remove()
        dd_node.style.width = width
        dd_node.style.minWidth = min_width

    def _change(self, raise_event=True, **event_args):
        keys = self.selected_keys
        if not keys:
            self._select_btn.text = self.placeholder
        else:
            self._select_btn.text = self.format_selected_text(len(keys), self._total)
        if raise_event:
            self.raise_event("change")

    def _mk_popover(self, init_node, **event_args):
        init_node(self._dd)

    def _open(self, **e):
        if not pop(self._select_btn, "shown"):
            pop(self._select_btn, "show")
            # invalidate these since the user has interacted with the component
            self._invalid = []

    def _close(self, **e):
        if pop(self._select_btn, "shown"):
            pop(self._select_btn, "hide")

    def _toggle(self, **e):
        if not pop(self._select_btn, "shown"):
            self._open()
        else:
            self._close()
