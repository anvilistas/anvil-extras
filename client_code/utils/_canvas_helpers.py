# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import Canvas as _Canvas
from anvil.js import get_dom_node as _dom_node
from anvil.js import window as _window

__version__ = "2.2.3"


def correct_canvas_resolution(canvas):
    """call this function in the reset event for a canvas element.
    It will reduce blurryness of canvas elements on retina screens"""
    assert isinstance(canvas, _Canvas), "expected a Canvas object as the first argument"
    dpr = max(_window.devicePixelRatio, 2)
    dom_c = _dom_node(canvas)
    rect = dom_c.getBoundingClientRect()
    new_width = int(rect.width * dpr)
    if dom_c.width == new_width:
        # we've done this scaling already
        return
    dom_c.width = new_width
    dom_c.height = int(rect.height * dpr)
    ctx = dom_c.getContext("2d")
    # scale all drawing options by the dpr
    # so we don't worry about the difference
    ctx.scale(dpr, dpr)
