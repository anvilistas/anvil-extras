# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil.js
from anvil import HtmlPanel as _HtmlPanel

from ..utils._component_helpers import _get_color, _html_injector, _spacing_property
from ._anvil_designer import SliderTemplate

try:
    from anvil.designer import in_designer
except ImportError:
    in_designer = False

__version__ = "3.1.0"

noui_version = "15.4.0"

_html_injector.cdn(
    f"https://cdn.jsdelivr.net/npm/nouislider@{noui_version}/dist/nouislider.min.css"
)

BAR_HEIGHT = "--ae-slider-height"
BAR_COLOR = "--ae-slider-bar_color"
HANDLE_SIZE = "--ae-slider-handle-size"


_html_injector.css(
    f"""
.ae-slider-container {{
  padding: 10px 0;
}}
.ae-slider-container.has-pips {{
  padding-bottom: 40px;
}}
.anvil-container-overflow, .anvil-panel-col {{
    overflow: visible;
}}
.noUi-connect {{
  background: var({BAR_COLOR});
}}
.noUi-horizontal {{
    height: var({BAR_HEIGHT})
}}
.noUi-horizontal .noUi-handle {{
    width: var({HANDLE_SIZE});
    height: var({HANDLE_SIZE});
    right: calc(var({HANDLE_SIZE}) / -2);
    top: calc((-2px + var({BAR_HEIGHT}) - var({HANDLE_SIZE}))/2);
    border-radius: 50%;
}}
.noUi-handle::before, .noUi-handle::after {{
    content: none
}}
"""
)

_Slider = anvil.js.import_from(
    "https://cdn.skypack.dev/pin/nouislider@v15.4.0-qwAfTOVKkfvhMhVnBPSn/mode=imports,min/optimized/nouislider.js"
).default


import json


def _as_list(x):
    return x if isinstance(x, list) else [x]


def _from_list(x):
    return x[0] if isinstance(x, list) else x


def _parse(s, force_list=False):
    if not isinstance(s, str):
        return s

    s = s.lower().strip()
    if not s:
        return None if not force_list else []
    if ("," in s or force_list) and s[0] != "[":
        s = "[" + s + "]"
    try:
        return json.loads(s)
    except Exception:
        return [] if force_list else s


try:
    # added in python 3.9 not currently available in skulpt
    _removeprefix = str.removeprefix
    _removesuffix = str.removesuffix
except AttributeError:

    def _removeprefix(s, prefix):
        return s[len(prefix) :] if s.startswith(prefix) else s

    def _removesuffix(s, suffix):
        return s[: len(s) - len(suffix)] if s.endswith(suffix) else s


def _wrap_formatter(formatter):
    fto = formatter["to"]
    ffrom = formatter["from"]

    def wrap_to(f: float, *args) -> str:
        s = fto(f)
        if not isinstance(s, str):
            raise TypeError(
                f"Custom formatter returned {type(s).__name__} (expected str)"
            )
        return s

    def wrap_from(s: str, *args) -> float:
        #### This function is called from javascript so accept *args
        if not isinstance(s, str):
            raise TypeError(
                f"got an unexpected value when trying to assign a value to the slider, (got {s})"
            )
        try:
            return ffrom(s)
        except Exception as e:
            try:
                # we may have just been give a number so do the obvious thing
                res = float(s)
                return int(res) if res.is_integer() else res
            except Exception:
                raise RuntimeError(f"your custom formatter raised an exception: {e!r}")

    return {"to": wrap_to, "from": wrap_from, "format_spec": formatter}


def _get_formatter(formatspec: str) -> dict:
    """
    Expecting a format spec e.g. '.2f'
    Or a simple string '£{:.2f}'
    """
    if isinstance(formatspec, dict):
        return _wrap_formatter(formatspec)
    if not isinstance(formatspec, str):
        raise TypeError("expected property format to be of type str")
    first = formatspec.find("{")
    last = formatspec.find("}")
    prefix = "" if first == -1 else formatspec[:first]
    suffix = "" if last == -1 else formatspec[last + 1 :]
    type = formatspec[len(formatspec) - 1] if last == -1 else formatspec[last - 1]

    def to_format(f: float, *args) -> str:
        # Used in javascript world so expects extra args
        try:
            return format(f, formatspec) if first == -1 else formatspec.format(f)
        except Exception:
            return f  # better just to return what was passed to us

    # this will raise an error if we have an invalid spec
    format(1.1, formatspec) if first == -1 else formatspec.format(1.1)

    def from_format(s: str, *args) -> float:
        # Used in javascript world so expects extra args
        if not isinstance(s, str):
            raise TypeError(
                f"got an unexpected value when trying to assign a value to the slider, (got {s})"
            )
        s = (
            _removesuffix(_removeprefix(s, prefix), suffix)
            .strip()
            .replace(",", "")
            .replace("_", "")
        )
        has_percent = type == "%" and s[len(s) - 1] == "%"
        if has_percent:
            s = s[: len(s) - 1]
        try:
            f = float(s)
        except Exception:
            return False
        if has_percent:
            f = f / 100
        return int(f) if f.is_integer() else f

    # noUiSlider requires a format like {from: (float) => str, to: (str) => float}
    return {"from": from_format, "to": to_format, "format_spec": formatspec}


def _prop_getter(prop):
    return lambda self: self._props[prop]


def _recreate_slider(self):
    self._dom_node.replaceChildren(self._slider_node)
    values = self.values
    try:
        self._parse_props()
        self._create_slider()
        if not in_designer:
            self.values = values
    except Exception as e:
        if in_designer:
            self._report_designer_error(e)
        else:
            raise e


def _slider_prop(prop, recreate=False):
    def setter(self, value):
        self._props[prop] = value
        if in_designer or recreate:
            return _recreate_slider(self)
        if prop == "format":
            value = _get_formatter(value)
            self._parsed_props["format"] = value
            pips = self._make_pips()
            self._slider.updateOptions({prop: value, "pips": pips})
        else:
            self._slider.updateOptions({prop: value})

    return property(_prop_getter(prop), setter)


def _slider_parse_prop(prop):
    def setter(self, value):
        self._props[prop] = value
        if in_designer:
            return _recreate_slider(self)
        parsed = _parse(value, prop == "pips")
        self._slider.updateOptions({prop: parsed})

    return property(_prop_getter(prop), setter)


def _color_prop(prop, var_name, default=None):
    def setter(self, value):
        self._props[prop] = value
        self._dom_node.style.setProperty(var_name, _get_color(value or default))

    return property(_prop_getter(prop), setter)


def _css_length_prop(prop, var_name, default):
    def setter(self, value):
        self._props[prop] = value
        value = value or default
        if isinstance(value, (int, float)) or str(value).isdigit():
            value = f"{value}px"
        self._dom_node.style.setProperty(var_name, value)

    return property(_prop_getter(prop), setter)


def _min_max_prop(prop):
    def getter(self):
        return self._parsed_props["range"][prop]

    def setter(self, value):
        r = self._parsed_props["range"]
        r[prop] = value
        self._props["range"] = r
        if in_designer:
            return _recreate_slider(self)
        self._slider.updateOptions({"range": r})

    return property(getter, setter)


def _pips_prop(prop):
    def setter(self, value):
        self._props[prop] = value
        pips = self._make_pips()
        self._toggle_has_pips(pips)
        self._slider.updateOptions({"pips": pips})

    return property(_prop_getter(prop), setter)


_defaults = {
    "animate": True,
    "start": 20,
    "step": None,
    "tooltips": False,
    "connect": False,
    "behaviour": "tap",
    "format": None,
    "pips": None,
    "pips_mode": None,
    "pips_values": [],
    "pips_density": -1,
    "pips_stepped": True,
    "margin": None,
    "padding": None,
    "limit": None,
    "range": None,
    "min": 0,
    "max": 100,
    "visible": True,
    "enabled": True,
    "spacing_above": "small",
    "spacing_below": "small",
    "value": None,
    "values": None,
    "formatted_value": None,
    "formatted_values": None,
    "bar_height": None,
    "handle_size": None,
    "color": None,
    "role": None,
}

_always = (
    "color",
    "enabled",
    "spacing_above",
    "spacing_below",
    "bar_height",
    "handle_size",
    "role",
)

_if_false = ("enabled", "visible")
_if_true = ("formatted_value", "formatted_values", "value", "values")

_error_msg = """
<div class='invalid-component'>
<i class="glyphicon glyphicon-remove"></i>
<div class="err">{}</div></div>
"""


class Slider(SliderTemplate):
    def __init__(self, **properties):
        # Any code you write here will run when the form opens.
        dom_node = self._dom_node = anvil.js.get_dom_node(self)
        dom_node.classList.add("ae-slider-container")

        self._slider_node = self.dom_nodes["ae-slider"]
        props = self._props = _defaults | properties

        self._slider = None
        try:
            self._parse_props()
            self._create_slider()
        except Exception as e:
            if in_designer:
                self._report_designer_error(e)
            else:
                raise e

        ###### PROPS TO INIT ######
        always = {p: props[p] for p in _always}
        if_true = {p: props[p] for p in _if_true if props[p] is not None}
        if_false = {p: props[p] for p in _if_false if not props[p]}
        self.init_components(**always, **if_false, **if_true)

    def _parse_props(self):
        props = self._props.copy()
        for prop in (
            "start",
            "connect",
            "margin",
            "padding",
            "limit",
            "pips_values",
        ):
            props[prop] = _parse(props[prop], prop == "pips_values")

        props["range"] = props["range"] or {"min": props["min"], "max": props["max"]}
        props["format"] = _get_formatter(props["format"] or ".2f")
        self._parsed_props = props

    def _create_slider(self):
        pips = self._make_pips()
        self._toggle_has_pips(pips)
        if self._slider is not None:
            self._slider.destroy()
        try:
            self._slider = _Slider.create(
                self._slider_node, self._parsed_props | {"pips": pips}
            )
        except Exception as e:
            if type(e) is anvil.js.ExternalError:
                e = e.original_error.message
            raise RuntimeError(repr(e).replace("noUiSlider", "Slider"))

        ###### EVENTS ######
        self._slider.on("slide", lambda a, h, *e: self.raise_event("slide", handle=h))
        self._slider.on("change", lambda a, h, *e: self.raise_event("change", handle=h))

    ###### VALUE PROPERTIES ######
    def _value_setter(self, val):
        self._slider.set(val)

    def _value(self):
        return _from_list(self._slider.get(True))

    def _values(self):
        return _as_list(self._slider.get(True))

    def _formatted_value(self):
        return _from_list(self._slider.get())

    def _formatted_values(self):
        return _as_list(self._slider.get())

    value = property(_value, _value_setter)
    values = property(_values, _value_setter)
    formatted_value = property(_formatted_value, _value_setter)
    formatted_values = property(_formatted_values, _value_setter)

    ###### noUiSlider PROPS ######
    connect = _slider_prop("connect", True)
    behaviour = _slider_prop("behaviour", True)
    margin = _slider_parse_prop("margin")
    padding = _slider_parse_prop("padding")
    limit = _slider_parse_prop("limit")
    step = _slider_parse_prop("step")
    start = _slider_parse_prop("start")
    range = _slider_parse_prop("range")
    min = _min_max_prop("min")
    max = _min_max_prop("max")
    tooltips = _slider_prop("tooltips")
    animate = _slider_prop("animate")
    format = _slider_prop("format")

    ###### PIPS PROPS ######
    pips = _pips_prop("pips")
    pips_mode = _pips_prop("pips_mode")
    pips_values = _pips_prop("pips_values")
    pips_density = _pips_prop("pips_density")
    pips_stepped = _pips_prop("pips_stepped")

    def _toggle_has_pips(self, pips):
        self._dom_node.classList.toggle("has-pips", bool(pips))

    def _make_pips(self):
        props = self._parsed_props
        pips = props["pips"]
        if not pips:
            return None
        elif pips is True:
            return {
                "format": props["format"],
                "mode": props["pips_mode"],
                "values": props["pips_values"],
                "density": props["pips_density"],
                "stepped": props["pips_stepped"],
            }
        elif isinstance(pips, dict):
            return pips
        else:
            raise TypeError(f"pips should be a bool or a dict, got {type(pips)}")

    ###### VISUAL PROPS ######

    @property
    def enabled(self):
        return not self._slider_node.getAttribute("disabled")

    @enabled.setter
    def enabled(self, value):
        if value:
            self._slider_node.removeAttribute("disabled")
        else:
            self._slider_node.setAttribute("disabled", True)

    bar_height = _css_length_prop("bar_height", BAR_HEIGHT, 18)
    handle_size = _css_length_prop("handle_size", HANDLE_SIZE, 34)
    color = _color_prop("color", BAR_COLOR)
    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")
    visible = _HtmlPanel.visible
    tag = _HtmlPanel.tag
    role = _HtmlPanel.role

    ###### METHODS ######
    def reset(self):
        self._slider.reset()
        self.raise_event("x-writeback")

    def _report_designer_error(self, e):
        self._dom_node.innerHTML = _error_msg.format(str(e))
