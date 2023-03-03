# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil.js import get_dom_node

from anvil_extras import ProgressBar
from anvil_extras.utils._component_helpers import _get_dom_node_id, _html_injector

from ._anvil_designer import IndeterminateTemplate

__version__ = "2.2.3"

_html_injector.css(ProgressBar.css)


class Indeterminate(IndeterminateTemplate):
    def __init__(self, track_colour, indicator_colour, **properties):
        dom_node = get_dom_node(self)
        dom_node.style.setProperty("background-color", indicator_colour)

        indicator_id = _get_dom_node_id(self.indicator_panel)
        css = f"""
#{indicator_id}:before {{
  background-color: {track_colour}
}}
"""
        _html_injector.css(css)
        self.role = "progress-track"
        self.indicator_panel.role = "indeterminate-progress-indicator"
        self.indicator_panel.background = indicator_colour
        self.init_components(**properties)
