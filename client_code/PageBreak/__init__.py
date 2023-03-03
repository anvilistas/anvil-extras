# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import anvil
from anvil.js.window import jQuery as _S

from ._anvil_designer import PageBreakTemplate

__version__ = "2.2.3"


class PageBreak(PageBreakTemplate):
    def __init__(self, margin_top=0, border="1px solid grey", **properties):
        dom_node = _S(anvil.js.get_dom_node(self))
        self.margin_node = dom_node.find(".margin-element")
        self.break_container = dom_node.find(".break-container")

        self.margin_top = margin_top
        self.border = border

        self.init_components(**properties)

    @property
    def margin_top(self):
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value):
        self.margin_node.css("margin-top", value)
        self._margin_top = value

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, value):
        self.break_container.css("border", value)
        self._border = value
