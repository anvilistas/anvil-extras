# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import anvil
import anvil.js

from ..utils import _component_helpers as helpers
from ._anvil_designer import PivotTemplate

__version__ = "1.6.0"

cdn = "https://cdnjs.cloudflare.com/ajax/libs"
pivottable_version = "2.23.0"
jqueryui_version = "1.11.4"
tags = [
    (f"{cdn}/pivottable/{pivottable_version}/pivot.min.css", "link"),
    (f"{cdn}/jqueryui/{jqueryui_version}/jquery-ui.min.js", "script"),
    (f"{cdn}/pivottable/{pivottable_version}/pivot.min.js", "script"),
]

_jquery = anvil.js.window.jQuery


try:
    assert "pivotUtilities" in _jquery.keys()
except AssertionError:
    for tag in tags:
        helpers.add_html_tag(*tag)
    assert "pivotUtilities" in _jquery.keys()


class Pivot(PivotTemplate):
    option_names = {
        "rows": "rows",
        "columns": "cols",
        "values": "vals",
        "aggregator": "aggregatorName",
    }

    def __init__(self, **properties):
        self.pivot_options = {
            option: properties[option] for option in self.option_names
        }
        dom_node = anvil.js.get_dom_node(self)
        self.pivot_node = dom_node.querySelector(".anvil-extras-pivot")
        self.init_components(**properties)

    def _init_pivot(self):
        options = {
            value: self.pivot_options[key] for key, value in self.option_names.items()
        }
        _jquery(self.pivot_node).pivotUI(self.items, options)

    def form_show(self, **event_args):
        self._init_pivot()
