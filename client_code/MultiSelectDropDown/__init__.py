# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil.js as _js
from anvil import HtmlPanel as _HtmlPanel
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S

from ._anvil_designer import MultiSelectDropDownTemplate

__version__ = "1.1.0"

_loaded = False


def _onload(e):
    global _loaded
    _loaded = True


def _wait_for_load(interval=0.005):
    global _loaded
    while not _loaded:
        from time import sleep

        sleep(interval)
    _loaded = False


def _add_script(s):
    dummy = _S(s)[0]  # let jquery pass the tag
    s = _document.createElement(dummy.tagName)
    for attr in dummy.attributes:
        s.setAttribute(attr.name, attr.value)
    s.textContent = dummy.textContent
    _document.head.appendChild(s)
    if not s.get("src"):
        return
    s.onload = s.onerror = _onload  # ignore errors
    _wait_for_load()


_add_script(
    """
<script>
  var orig_offset = jQuery.fn.offset
  jQuery.fn.offset = function() {
      if (!this[0].isConnected) {
          return 0; // prevent warning in output
      }
      return orig_offset.call(this);
  }
</script >
"""
)

_add_script(
    """
<script
  src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/js/bootstrap-select.min.js">
</script>
"""
)


_add_script(
    """
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/css/bootstrap-select.min.css"
>
"""
)

_S.fn.selectpicker.Constructor.BootstrapVersion = "3"


defaults = {
    "align": "left",
    "placeholder": "None Selected",
    "enable_filtering": False,
    "multiple": True,
    "enabled": True,
    "spacing_below": "small",
    "spacing_above": "small",
}


def component_property(internal, jquery, fn=None):
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


def spacing_property(which):
    def getter(self):
        return getattr(self, "_spacing_" + which)

    def setter(self, value):
        self._dom_node.classList.remove(
            f"anvil-spacing-{which}-{getattr(self, '_spacing_' + which, '')}"
        )
        self._dom_node.classList.add(f"anvil-spacing-{which}-{value}")
        setattr(self, "_spacing_" + which, value)

    return property(getter, setter, None, which)


class MultiSelectDropDown(MultiSelectDropDownTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self._init = False

        self._dom_node = _js.get_dom_node(self)
        self._el = _S(self._dom_node).find("select")

        _S(self._dom_node).html("").append(self._el)
        # remove all the script tags before they load into the dom

        self._values = {}
        # Any code you write here will run when the form opens.
        properties = defaults | properties

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
        self._el.append(self._clean_items(value))
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

    multiple = component_property("multiple", "multiple")
    placeholder = component_property("placeholder", "title")
    enable_filtering = component_property("enable_filtering", "data-live-search")
    enabled = component_property("enabled", "disabled", lambda v: not v)

    visible = _HtmlPanel.visible

    spacing_above = spacing_property("above")
    spacing_below = spacing_property("below")

    ##### EVENTS #####
    def change(self, *e):
        return self.raise_event("change")

    ##### PRIVATE METHODS #####
    def _clean_dict_item(self, item, index):
        sentinal = object()

        # if they only set a key and not a value then use the key as the value
        value = item.get("value", sentinal)
        if value is sentinal:
            item["value"] = item.get("key")

        title = repr(item.get("title", ""))
        icon = repr(item.get("icon", "")).replace(":", "-")
        subtext = repr(item.get("subtext", ""))
        disabled = not item.get("enabled", True)

        option = f"""<option {'disabled' if disabled else ''}
                         {f'data-icon={icon}' if icon else ''}
                         {f'data-subtext={subtext}' if subtext else ''}
                         {f'title={title}' if title else ''}
                         value={index}>
                           {item.get('key')}
                 </option>"""

        return option, item["value"]

    def _clean_items(self, items):

        options = []
        value_dict = {}

        for idx, val in enumerate(items):
            idx = str(idx)

            if isinstance(val, str):
                if val == "---":
                    options.append("<option data-divider='true'/>")
                else:
                    value_dict[idx] = val
                    options.append(f"<option value={idx}>{val}</option>")
            elif isinstance(val, (tuple, list)):
                key = val[0]
                if not isinstance(key, str):
                    raise TypeError(
                        f"expectected a tuple of the form str, value in items at index {idx}"
                    )
                if len(val) != 2:
                    raise ValueError(f"expectected a tuple of length 2 at index {idx}")
                value_dict[idx] = val[1]
                options.append(f"<option value={idx}>{val[0]}</option>")

            elif isinstance(val, dict):
                option, value = self._clean_dict_item(val, idx)
                value_dict[idx] = value
                options.append(option)

        self._values = value_dict
        return _S("\n".join(options))
