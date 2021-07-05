# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import anvil
from anvil.js.window import jQuery as _S

from ._anvil_designer import PageBreakTemplate

__version__ = "1.5.1"


class PageBreak(PageBreakTemplate):
    def __init__(self, margin_top, **properties):
        self.margin_node = _S(anvil.js.get_dom_node(self)).find(".margin-element")
        self.margin_top = margin_top
        self.init_components(**properties)

    @property
    def margin_top(self):
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value):
        self.margin_node.css("margin-top", value)
        self._margin_top = value
