# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import anvil

from ..utils._component_helpers import _css_length
from ._anvil_designer import PageBreakTemplate

__version__ = "3.0.0"


class PageBreak(PageBreakTemplate):
    def __init__(self, **properties):
        self._props = properties
        self.init_components(**properties)

    @property
    def margin_top(self):
        return self._props.get("margin_top")

    @margin_top.setter
    def margin_top(self, value):
        self._props["margin_top"] = value
        self.dom_nodes["ae-page-break-margin-element"].style.marginTop = _css_length(
            value
        )

    @property
    def border(self):
        return self._props.get("border")

    @border.setter
    def border(self, value):
        self._props["border"] = value
        self.dom_nodes["ae-page-break-container"].style.border = value
