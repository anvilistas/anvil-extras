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

__version__ = "2.2.3"

pivottable_version = "2.23.0"
jqueryui_version = "1.11.4"

prefix = "https://cdnjs.cloudflare.com/ajax/libs"
dependencies = [
    f"{prefix}/pivottable/{pivottable_version}/pivot.min.css",
    f"{prefix}/pivottable/{pivottable_version}/pivot.min.js",
]
jqueryui = f"{prefix}/jqueryui/{jqueryui_version}/jquery-ui.min.js"

_jquery = anvil.js.window.jQuery

helpers._html_injector.css(
    """.anvil-container-overflow, .anvil-panel-col {
        overflow: visible;
    }
    .anvil-extras-pivot-container {
        display: grid
    }
    .pivot-placeholder {
        overflow: auto
    }
    """
)

if "ui" not in _jquery.keys():
    helpers._html_injector.cdn(jqueryui)

try:
    assert tuple(int(x) for x in _jquery.ui.version.split(".")) >= (1, 9, 0)
except AssertionError:
    raise AssertionError("Incompatible jqueryui version already installed")

try:
    assert "pivotUtilities" in _jquery.keys()
except AssertionError:
    for dependency in dependencies:
        helpers._html_injector.cdn(dependency)
    assert "pivotUtilities" in _jquery.keys()


class Pivot(PivotTemplate):
    option_names = {
        "rows": "rows",
        "columns": "cols",
        "values": "vals",
        "aggregator": "aggregatorName",
    }

    def __init__(self, **properties):
        self.pivot_initiated = False
        self.pivot_options = {
            option: properties[option] for option in self.option_names
        }
        dom_node = anvil.js.get_dom_node(self)
        self.pivot_node = dom_node.querySelector(".anvil-extras-pivot")
        dom_node.querySelector("script").remove()
        dom_node.classList.add("anvil-extras-pivot-container")
        self.init_components(**properties)

    def _init_pivot(self):
        card_node = self.pivot_node.closest(".anvil-role-card")
        if card_node:
            card_node.style.overflow = "visible"
        options = {
            value: self.pivot_options[key] for key, value in self.option_names.items()
        }
        _jquery(self.pivot_node).pivotUI(self.items, options)

    def form_show(self, **event_args):
        if not self.pivot_initiated:
            self._init_pivot()
            self.pivot_initiated = True
