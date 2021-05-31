# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil.js import get_dom_node
from anvil.js.window import document

from anvil_extras import ProgressBar, session

from ._anvil_designer import IndeterminateTemplate

__version__ = "1.3.1"

session.style_injector.inject(ProgressBar.css)


class Indeterminate(IndeterminateTemplate):
    def __init__(self, track_colour, indicator_colour, **properties):
        dom_node = get_dom_node(self)
        dom_node.style.setProperty("background-color", indicator_colour)

        indicator_id = session.get_dom_node_id(self.indicator_panel)
        css = f"""
#{indicator_id}:before {{
  background-color: {track_colour}
}}
"""
        session.style_injector.inject(css)
        self.role = "progress-track"
        self.indicator_panel.role = "indeterminate-progress-indicator"
        self.indicator_panel.background = indicator_colour
        self.init_components(**properties)
