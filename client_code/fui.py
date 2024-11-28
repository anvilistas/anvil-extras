# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js import import_from
from anvil.js.window import window as _W

__version__ = "3.1.0"

try:
    # support preloaded FloatingUIDOM
    FloatingUIDOM = _W.FloatingUIDOM
except AttributeError:
    # https://floating-ui.com/
    FloatingUIDOM = import_from(
        "https://cdn.jsdelivr.net/npm/@floating-ui/dom@1.6.10/+esm"
    )

_static_arrow_position = {
    "top": "bottom",
    "right": "left",
    "bottom": "top",
    "left": "right",
}


def size_middleware():
    def apply(context):
        availableHeight = context["availableHeight"]
        elements = context["elements"]
        elements.floating.style.maxHeight = f"{availableHeight}px"

    return {"apply": apply}


def auto_update(
    reference_el,
    floating_el,
    *,
    placement="bottom",
    strategy="absolute",
    offset=None,
    shift={"padding": 5},
    hide={"padding": 15},
    arrow=None,
):
    """starts auto updating position of floating element to a reference element
    returns a cleanup function
    if using arrow, arrow should be an HTMLElement
    call this function in x-anvil-page-added
    call the cleanup in x-anvil-page-removed"""

    offset = 11 if arrow else 4

    def update(*args):
        middleware = [
            FloatingUIDOM.offset(offset),
            FloatingUIDOM.flip(),
            FloatingUIDOM.shift(shift),
            FloatingUIDOM.hide(hide),
            FloatingUIDOM.size(size_middleware()),
        ]

        if arrow:
            middleware.append(FloatingUIDOM.arrow({"element": arrow}))

        rv = FloatingUIDOM.computePosition(
            reference_el,
            floating_el,
            {
                "placement": placement,
                "strategy": strategy,
                "middleware": middleware,
            },
        )
        floating_el.style.left = f"{rv.x}px"
        floating_el.style.top = f"{rv.y}px"

        middlewareData = rv.middlewareData

        if "hide" in middlewareData:
            hidden = middlewareData.hide.referenceHidden
            floating_el.style.visibility = "hidden" if hidden else "visible"

        main_axis = rv.placement.split("-")[0]
        static_side = _static_arrow_position.get(main_axis)

        if arrow and "arrow" in middlewareData:
            x = middlewareData.arrow.get("x")
            y = middlewareData.arrow.get("y")

            arrow.style.left = "" if x is None else f"{x}px"
            arrow.style.top = "" if y is None else f"{y}px"
            arrow.style.right = ""
            arrow.style.bottom = ""
            if static_side:
                arrow.style[static_side] = "-11px"

        floating_el.classList.remove("left", "right", "top", "bottom")
        floating_el.classList.add(main_axis)

    return FloatingUIDOM.autoUpdate(reference_el, floating_el, update)
