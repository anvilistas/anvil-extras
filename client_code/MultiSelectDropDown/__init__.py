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
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S

from ..session import style_injector
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
    s.onload = s.onerror = _onload  # ignore errors
    _wait_for_load()


_add_script(
    """
<script
    src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-multiselect/0.9.15/js/bootstrap-multiselect.min.js"
    integrity="sha512-aFvi2oPv3NjnjQv1Y/hmKD7RNMendo4CZ2DwQqMWzoURKxcqAoktj0nNG4LU8m23+Ws9X5uVDD4OXLqpUVXD5Q=="
    crossorigin="anonymous">
</script>
"""
)

_add_script(
    """
<link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-multiselect/0.9.15/css/bootstrap-multiselect.css"
    integrity="sha512-EvvoSMXERW4Pe9LjDN9XDzHd66p8Z49gcrB7LCUplh0GcEHiV816gXGwIhir6PJiwl0ew8GFM2QaIg2TW02B9A=="
    crossorigin="anonymous"
/>
"""
)

style_injector.inject(
    """
.anvil-container, .anvil-container div {
    overflow: visible;
}
.multiselect-filter  i {
    position: absolute;
    padding: 0 5px;
    margin-left: 2px;
    top: 50%;
    left: 0;
    color: grey;
    transform: translate3d(0, -50%, 0);
    z-index: 3;
}
.multiselect-filter  input {
    border-radius: 4px;
    padding-left: 25px;
}
.multiselect-container.dropdown-menu>.active>a, .multiselect-container.dropdown-menu>.active>a:hover, .multiselect-container.dropdown-menu>.active>a:focus {
    background: #d3d3d3;
    color: black;
}
"""
)


defaults = {
    "align": "left",
    "placeholder": "None Selected",
    "number_displayed": 3,
    "filter_placeholder": "search",
    "enable_filtering": False,
    "multiple": True,
}


class MultiSelectDropDown(MultiSelectDropDownTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self._dom_node = _js.get_dom_node(self)
        self._el = _S(self._dom_node).find("select")

        _S(self._dom_node).html("").append(self._el)
        # remove all the script tags before they load into the dom

        self._values = {}
        # Any code you write here will run when the form opens.
        properties = defaults | properties

        if not properties["multiple"]:
            self._el.removeAttr("multiple")

        self._el.multiselect(
            {
                "onChange": self.change,
                "nonSelectedText": properties["placeholder"],
                "enableCaseInsensitiveFiltering": properties["enable_filtering"],
                "filterPlaceholder": properties["filter_placeholder"],
                "numberDisplayed": properties["number_displayed"],
            }
        )

        self._btn = self._el.siblings(".btn-group").find("button")
        self._filter = properties["enable_filtering"]
        self._el.ready(self._ready)
        self.init_components(**properties)

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, value):
        self._align = value
        self._btn.css("textAlign", value)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._el.multiselect("dataprovider", self._clean_items(value))
        self._items = value

    @property
    def selected(self):
        return list(
            map(lambda e: self._values[e.value], _S("option:selected", self._el))
        )

    @selected.setter
    def selected(self, values):
        if not isinstance(values, (list, tuple)):
            values = [values]

        to_select = []
        for key, val in self._values.items():
            if val in values:
                to_select.append(key)

        self._el.multiselect("deselectAll", False)
        self._el.multiselect("select", to_select)

    ##### EVENTS #####
    def change(self, *e):
        return self.raise_event("change")

    ##### PRIVATE METHODS #####
    def _clean_dict_item(self, index, item):

        sentinal = object()

        value = item.get("value", sentinal)
        if value is sentinal:
            item["value"] = item.get("key")

        def convert(old, new):
            old = item.pop(old, sentinal)
            if old is not sentinal:
                item[new] = old

        convert("key", "label")
        convert("tooltip", "title")

        return item

    def _clean_items(self, items):

        item_dict = []
        value_dict = {}

        for idx, val in enumerate(items):
            idx = str(idx)

            if isinstance(val, str):
                if val == "---":
                    item_dict.append({"attributes": {"role": "divider"}})
                else:
                    item_dict.append({"label": val, "value": idx})
                    value_dict[idx] = val
            elif isinstance(val, (tuple, list)):
                key = val[0]
                if not isinstance(key, str):
                    raise TypeError(
                        f"expectected a tuple of the form str, value in items at index {idx}"
                    )
                if len(val) != 2:
                    raise ValueError(f"expectected a tuple of length 2 at index {idx}")
                item_dict.append({"label": val[0], "value": idx})
                value_dict[idx] = val[1]
            elif isinstance(val, dict):
                item = self._clean_dict_item(idx, val)
                item["value"], value_dict[idx] = idx, item["value"]
                item_dict.append(item)

        self._values = value_dict
        return item_dict

    def _ready(self, *e, **event_args):
        """This method is called when the HTML panel is shown on the screen"""
        if self._filter:
            i = _document.createElement("i")
            i.className = "fa fas fa-search"
            input_group = self._dom_node.querySelector(
                ".multiselect-filter .input-group"
            )
            input_group.replaceChild(i, input_group.firstElementChild)
            input_group.removeChild(input_group.querySelector("span"))
