# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil.js import get_dom_node

from anvil_extras import ProgressBar
from anvil_extras.utils._component_helpers import (
    _css_length,
    _get_color,
    _html_injector,
)

from ._anvil_designer import IndeterminateTemplate

__version__ = "3.6.0"

_html_injector.css(ProgressBar.css)


class Indeterminate(IndeterminateTemplate):
    def __init__(self, **properties):
        self.indicator_dom_node = get_dom_node(self.indicator_panel)
        self.dom_node = get_dom_node(self)
        self._props = properties
        self.role = "ae-progress-track"
        self.indicator_panel.role = "ae-indeterminate-progress-indicator"
        self.init_components(**properties)

    @property
    def height(self):
        return self._props.get("height")

    @height.setter
    def height(self, value):
        self._props["height"] = value
        self.indicator_dom_node.style.setProperty("height", _css_length(value or 3))

    @property
    def track_colour(self):
        return self._props.get("track_colour")

    @track_colour.setter
    def track_colour(self, value):
        self._props["track_colour"] = value
        self.dom_node.style.setProperty(
            "--ae-track-colour", value and _get_color(value)
        )

    @property
    def indicator_colour(self):
        return self._props.get("indicator_colour")

    @indicator_colour.setter
    def indicator_colour(self, value):
        self._props["indicator_colour"] = value
        self.dom_node.style.setProperty("background-color", _get_color(value))
