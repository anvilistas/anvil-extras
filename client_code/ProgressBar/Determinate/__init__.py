# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil.js import get_dom_node

from anvil_extras import ProgressBar
from anvil_extras.utils._component_helpers import _html_injector

from ._anvil_designer import DeterminateTemplate

__version__ = "2.2.3"

_html_injector.css(ProgressBar.css)


class Determinate(DeterminateTemplate):
    def __init__(self, track_colour, indicator_colour, **properties):
        self.indicator_dom_node = get_dom_node(self.indicator_panel)
        self.role = "progress-track"
        self.indicator_panel.role = "progress-indicator"
        self.background = track_colour
        self.indicator_panel.background = indicator_colour
        self.init_components(**properties)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.indicator_dom_node.style.setProperty("width", f"{value:%}")
