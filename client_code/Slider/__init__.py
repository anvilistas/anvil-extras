from anvil import HtmlPanel as _HtmlPanel
from anvil import *
from anvil.js import get_dom_node as _get_dom_node
from anvil.js import window as _window

from ..utils._component_helpers import _add_script, _get_color, _spacing_property
from ._anvil_designer import SliderTemplate

__version__ = "1.2.0"


_add_script(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/nouislider@15.1.1/dist/nouislider.css"></link>'
)
_add_script(
    """
<style>
.anvil-slider-container {
  padding: 10px 0;
}
.anvil-slider-container.has-pips {
  padding-bottom: 40px;
}
.anvil-container-overflow, .anvil-panel-col {
    overflow: visible;
}
.noUi-connect {
  background: var(--primary);
}

.noUi-horizontal .noUi-handle {
    width: 34px;
    height: 34px;
    right: -17px;
    top: -10px;
    border-radius: 50%;
}
.noUi-handle::before, .noUi-handle::after {
    content: none
}
</style>"""
)

_add_script(
    '<script crossorigin src="https://cdn.jsdelivr.net/npm/nouislider@15.1.1/dist/nouislider.js"></script>'
)
_Slider = _window.noUiSlider


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


def _get_formatter(formatspec: str) -> dict:
    """
    Expecting a format spec e.g. '.2f'
    Or a simple string '£{:.2f}'
    """
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
            raise TypeError(f"got an unexpected value for handle, (got {s})")
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
        return f

    # noUiSlider requires a format like {from: (float) => str, to: (str) => float}
    return {"from": from_format, "to": to_format, "format_spec": formatspec}


def _prop_getter(prop, fget=None):
    return lambda self: self._props[prop] if fget is None else fget(self._props[prop])


def _slider_prop(prop, fset=None, fget=None):
    def setter(self, value):
        self._props[prop] = value if fset is None else fset(value)
        self._slider.updateOptions({prop: value})

    return property(_prop_getter(prop, fget), setter)


def _min_max_prop(prop):
    def getter(self):
        return self._props["range"][prop]

    def setter(self, value):
        r = self._props["range"]
        r[prop] = value
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
}


class Slider(SliderTemplate):
    def __init__(self, **properties):
        # Any code you write here will run when the form opens.
        dom_node = self._dom_node = _get_dom_node(self)
        dom_node.classList.add("anvil-slider-container")

        self._slider_node = dom_node.querySelector(".anvil-slider")
        # remove the script to stop them loading
        while dom_node.firstElementChild:
            dom_node.removeChild(dom_node.firstElementChild)
        dom_node.append(self._slider_node)

        props = self._props = _defaults | properties

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

        pips = self._make_pips()
        self._toggle_has_pips(pips)
        try:
            self._slider = _Slider.create(self._slider_node, props | {"pips": pips})
        except Exception as e:
            raise RuntimeError(repr(e).replace("noUiSlider", "Slider"))

        ###### EVENTS ######
        self._slider.on("slide", lambda a, h, *e: self.raise_event("slide", handle=h))
        self._slider.on("change", lambda a, h, *e: self.raise_event("change", handle=h))

        ###### PROPS TO INIT ######
        self.init_components(
            **{
                prop: props[prop]
                for prop in (
                    "color",
                    "enabled",
                    "visible",
                    "spacing_above",
                    "spacing_below",
                    "formatted_value",
                    "formatted_values",
                    "value",
                    "values",
                )
                if props[prop] is not None
            }
        )

    ###### VALUE PROPERTIES ######
    @property
    def _convert(self):
        f = self._props["format"]["from"]

        def convert(x: str) -> float:
            res = f(x)
            return x if res is False else res

        return convert

    def _value_setter(self, val):
        self._slider.set(val)

    def _value(self):
        return self._convert(_from_list(self._slider.get()))

    def _values(self):
        return list(map(self._convert, _as_list(self._slider.get())))

    def _formatted_value(self):
        return _from_list(self._slider.get())

    def _formatted_values(self):
        return _as_list(self._slider.get())

    value = property(_value, _value_setter)
    values = property(_values, _value_setter)
    formatted_value = property(_formatted_value, _value_setter)
    formatted_values = property(_formatted_values, _value_setter)

    ###### noUiSlider PROPS ######
    connect = _slider_prop("connect")  # not dynamic
    behaviour = _slider_prop("behaviour")  # not dynamic
    margin = _slider_prop("margin")
    padding = _slider_prop("padding")
    limit = _slider_prop("limit")
    step = _slider_prop("step")
    start = _slider_prop("start")
    range = _slider_prop("range")
    min = _min_max_prop("min")
    max = _min_max_prop("max")
    tooltips = _slider_prop("tooltips")
    animate = _slider_prop("animate")
    format = _slider_prop(
        "format", fset=lambda s: _get_formatter(s), fget=lambda d: d["format_spec"]
    )

    ###### PIPS PROPS ######
    pips = _pips_prop("pips")
    pips_mode = _pips_prop("pips_mode")
    pips_values = _pips_prop("pips_values")
    pips_density = _pips_prop("pips_density")
    pips_stepped = _pips_prop("pips_stepped")

    def _toggle_has_pips(self, pips):
        self._dom_node.classList.toggle("has-pips", bool(pips))

    def _make_pips(self):
        props = self._props
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

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._dom_node.style.setProperty("--primary", _get_color(value))

    spacing_above = _spacing_property("above")
    spacing_below = _spacing_property("below")
    visible = _HtmlPanel.visible

    ###### METHODS ######
    def reset(self):
        self._slider.reset()
        self.raise_event("x-writeback")
