# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil.js as _js
from anvil import HtmlPanel as _HtmlPanel
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S

from ..utils._component_helpers import _html_injector, _spacing_property
from ._anvil_designer import MultiSelectDropDownTemplate

__version__ = "1.9.0"

_html_injector.script(
    """
var orig_offset = jQuery.fn.offset
jQuery.fn.offset = function() {
    if (!this[0].isConnected) {
        return 0; // prevent warning in output
    }
    return orig_offset.call(this);
}
"""
)


# If we update this - check the form_hide/form_show behaviour still works
bs_select_version = "1.13.18"
prefix = "https://cdn.jsdelivr.net/npm/bootstrap-select@"
suffix = "/dist/js/bootstrap-select.min"

_html_injector.cdn(f"{prefix}{bs_select_version}/dist/js/bootstrap-select.min.js")
_html_injector.cdn(f"{prefix}{bs_select_version}/dist/css/bootstrap-select.min.css")


_S.fn.selectpicker.Constructor.BootstrapVersion = "3"


def off_dd_click(e):
    # see bug #271
    if not e.target.closest(".bootstrap-select"):
        _S(_document).trigger("click.bs.dropdown.data-api")


_document.addEventListener("click", off_dd_click, True)


_defaults = {
    "align": "left",
    "placeholder": "None Selected",
    "enable_filtering": False,
    "multiple": True,
    "enabled": True,
    "spacing_below": "small",
    "spacing_above": "small",
    "enable_select_all": False,
}


def _component_property(internal, jquery, fn=None):
    def getter(self):
        return getattr(self, "_" + internal)

    def setter(self, value):
        setattr(self, "_" + internal, value)
        value = value if fn is None else fn(value)
        if value:
            self._el.attr(jquery, value)
        else:
            self._el.attr(jquery, None)

        if self._init:
            self._el.selectpicker("refresh")
            self._el.selectpicker("render")

    return property(getter, setter, None, internal)


class MultiSelectDropDown(MultiSelectDropDownTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self._init = False

        self._dom_node = _js.get_dom_node(self)
        self._el = _S(self._dom_node).find("select")

        _S(self._dom_node).html("").append(self._el)
        # remove all the script tags before they load into the dom

        self._values = {}
        # Any code you write here will run when the form opens
        properties = _defaults | properties
        properties["items"] = properties["items"] or []

        self.init_components(**properties)

        self._el.selectpicker()
        self._el.on("changed.bs.select", self.change)
        self._init = True

    ##### PROPERTIES #####
    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, value):
        if value == "full":
            text_align = None
            width = "100%"
        else:
            text_align = value
            width = None
        self._dom_node.style.textAlign = text_align
        self._el.attr("data-width", width)
        self._align = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        selected = self.selected
        self._el.children().remove()
        options, values = _clean_items(value)
        self._el.append(options)
        self._values = values
        self._items = value
        self.selected = selected
        self._el.selectpicker("refresh")
        self._el.selectpicker("render")

    @property
    def selected(self):
        return list(
            map(
                lambda e: self._values[e.value],
                filter(lambda e: e.value != "", _S("option:selected", self._el)),
            )
        )

    @selected.setter
    def selected(self, values):
        if not isinstance(values, (list, tuple)):
            values = [values]
        to_select = []
        for key, val in self._values.items():
            if val in values:
                to_select.append(key)
        self._el.selectpicker("val", to_select)

    multiple = _component_property("multiple", "multiple")
    # the placeholder is not dynamic - this seems to be a bug in the javascript library
    placeholder = _component_property("placeholder", "title")
    enable_filtering = _component_property("enable_filtering", "data-live-search")
    enabled = _component_property("enabled", "disabled", lambda v: not v)
    enable_select_all = _component_property("enable_select_all", "data-actions-box")

    @property
    def visible(self):
        return _HtmlPanel.visible.__get__(self, type(self))

    @visible.setter
    def visible(self, val):
        self._el.data("selectpicker")["$bsContainer"].toggleClass(
            "visible-false", not val
        )
        _HtmlPanel.visible.__set__(self, val)

    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")

    ##### EVENTS #####
    def change(self, *e):
        return self.raise_event("change")

    def _form_hide(self, **event_args):
        # this is a bit of a hack - we're using the libraries private methods for this
        bs_container = self._el.data("selectpicker")["$bsContainer"]
        bs_container.removeClass("anvil-popover").attr("popover_id", None).detach()

    def _form_show(self, **event_args):
        popover = self._dom_node.closest(".anvil-popover")
        if popover is None:
            return
        pop_id = popover.getAttribute("popover_id")
        bs_container = self._el.data("selectpicker")["$bsContainer"]
        bs_container.addClass("anvil-popover").attr("popover_id", pop_id)


##### PRIVATE Functions #####


def _option_from_str(item: str, idx: str) -> tuple:
    key = value = item
    if item == "---":
        return "<option data-divider='true'></option>", object()  # dummy value
    else:
        return f"<option value={idx}>{key}</option>", value


def _option_from_tuple(item: tuple, idx: int) -> tuple:
    key, value = item
    if not isinstance(key, str):
        raise TypeError(
            f"expectected a tuple of the form str, value in items at idx {idx}"
        )
    return f"<option value={idx}>{key}</option>", value


def _option_from_dict(item: dict, idx: int) -> tuple:
    sentinel = object()

    # if they only set a key and not a value then use the key as the value
    value = item.get("value", sentinel)
    if value is sentinel:
        value = item.get("key")

    title = repr(item.get("title", ""))
    icon = repr(item.get("icon", "")).replace(":", "-")
    subtext = repr(item.get("subtext", ""))
    disabled = not item.get("enabled", True)

    option = f"""<option {'disabled' if disabled else ''}
                        {f'data-icon={icon}' if icon else ''}
                        {f'data-subtext={subtext}' if subtext else ''}
                        {f'title={title}' if title else ''}
                        value={idx}>
                        {item.get('key')}
                </option>"""

    return option, value


def _clean_items(items):
    options = []
    value_dict = {}

    for idx, item in enumerate(items):

        if isinstance(item, str):
            option, value = _option_from_str(item, idx)
        elif isinstance(item, (tuple, list)):
            option, value = _option_from_tuple(item, idx)
        elif isinstance(item, dict):
            option, value = _option_from_dict(item, idx)
        else:
            raise TypeError(f"Invalid item at index {idx} (got type {type(item)})")

        # use strings since the value from jquery is always a string
        value_dict[str(idx)] = value
        options.append(option)

    return _S("\n".join(options)), value_dict
