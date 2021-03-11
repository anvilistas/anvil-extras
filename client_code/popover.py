# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/anvilistas/anvil-extras
#
#
# for more information visit the w3 bootstrap popover page
# https://www.w3schools.com/bootstrap4/bootstrap_ref_js_popover.asp
#
# or the bootstrap popover page for v 3.3.7
# https://bootstrapdocs.com/v3.3.6/docs/javascript/#popovers
#

from random import choice as _random_choice
from string import ascii_letters as _letters

import anvil as _anvil
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S
from anvil.js.window import window as _window

__version__ = "1.0.0"


def popover(
    self,
    content,
    title="",
    placement="right",
    trigger="click",
    animation=True,
    delay={"show": 100, "hide": 100},
    max_width=None,
    auto_dismiss=True,
):
    """should be called by a button or link
    content - either text or an anvil component or Form
    placement -  right, left, top, bottom (for left/right best to have links and buttons inside flow panels)
    trigger - manual, focus, hover, click (can be a combination of two e.g. 'hover focus')
    animation - True or False
    delay - {'show': 100, 'hide': 100}
    max_width - bootstrap default is 276px you might want this wider

    if the content is a form then the form will have an attribute self.popper added
    """
    html = not isinstance(content, str)
    if html:
        content.popper = self  # add the popper to the content form
        content = _anvil.js.get_dom_node(content)  # get the dom node

    max_width = _default_max_width if max_width is None else max_width

    # can effect the title of the popover so temporarily set it to ''
    tooltip, self.tooltip = self.tooltip, ""

    popper_id = _get_random_string(5)
    popper_element = _get_jquery_popper_element(self)

    if trigger == "stickyhover":
        trigger = "manual"
        popper_element.on(
            "mouseenter",
            lambda e: None if pop(self, "is_visible") else pop(self, "show"),
        ).on(
            "mouseleave",
            lambda e: None
            if _S("[popover_id={}]:hover".format(popper_id))
            else pop(self, "hide"),
        )
        _set_sticky_hover()
        _sticky_popovers.add(popper_id)

    popper_element.popover(
        {
            "content": content,
            "title": title,
            "placement": placement,
            "trigger": trigger,
            "animation": animation,
            "delay": delay,
            "html": html,
            "template": _template.format(popper_id, max_width),
            "container": "body",
        }
    )

    if tooltip:
        self.tooltip = tooltip
        # otherwise the tooltip doesn't work for Buttons
        popper_element.attr("title", tooltip)

    popper_element.on(
        "show.bs.popover",
        lambda e: _visible_popovers.update({popper_id: popper_element})
        if auto_dismiss
        else None,
    ).on("hide.bs.popover", lambda e: _visible_popovers.pop(popper_id, None)).addClass(
        "anvil-popover"
    ).attr(
        "popover_id", popper_id
    )


def pop(self, behavior):
    """behaviour can be any of
    show, hide, toggle, destroy (included with bootstrap 3.3.7)

    features added not in bootstrap 3.3.7 docs:
    update  - updates position of popover - useful for dynamic content that changes the size of the popover
    shown: returns True or False if the popover is visible - note a popover will only be visible after it has animated onto screen so may need to sleep(.15) before calling
    is_visible: same as shown
    """
    popper_element = _get_jquery_popper_element(self)
    if behavior == "shown" or behavior == "is_visible":
        return _is_visible(popper_element)
    elif behavior == "update":
        return _update_positions()
    if behavior == "hide":
        popper_element.data(
            "bs.popover"
        ).inState.click = (
            False  # see bug https://github.com/twbs/bootstrap/issues/16732
        )
    elif behavior == "show":
        popper_element.data("bs.popover").inState.click = True
    elif behavior == "toggle":
        current = popper_element.data("bs.popover").inState.click
        popper_element.data("bs.popover").inState.click = not current
    try:
        popper_element.popover(behavior)
    except:
        raise ValueError("unrecognized behavior: {}".format(behavior))


# this is the default behavior
def dismiss_on_outside_click(dismiss=True):
    """hide popovers when a user clicks outside the popover
    this is the default behavior
    """
    _document.body.removeEventListener("click", _hide_popovers_on_outside_click)
    if dismiss:
        _document.body.addEventListener("click", _hide_popovers_on_outside_click, True)


_default_max_width = ""


def set_default_max_width(width):
    """update the default max width - this is 276px by default - useful for wider components"""
    global _default_width
    _default_width = width


for _ in [_anvil.Button, _anvil.Link, _anvil.Label, _anvil.Image]:
    _.popover = popover
    _.pop = pop

######## helper functions ########

_sticky_popovers = set()


def _sticky_leave(e):
    popper_element = None
    popover_id = _S(e.currentTarget).attr("popover_id")
    if popover_id in _sticky_popovers and not _S(
        "[popover_id={}]:hover".format(popover_id)
    ):
        popper_element = _visible_popovers.get(popover_id)
    if popper_element is not None:
        popper_element.data(
            "bs.popover"
        ).inState.click = (
            False  # see bug https://github.com/twbs/bootstrap/issues/16732
        )
        popper_element.popover("hide")


def _set_sticky_hover():
    if not _sticky_popovers:
        _S("body").on("mouseleave", ".popover", _sticky_leave)


def _update_positions(*args):
    _S(".popover").addClass("PopNoTransition").popover("show").removeClass(
        "PopNoTransition"
    )


_window.addEventListener("resize", _update_positions)


def _hide(popover_id, visible_popovers):
    popper = visible_popovers[popover_id].popover("hide")
    # hack for click https://github.com/twbs/bootstrap/issues/16732
    try:
        popper.data("bs.popover").inState.click = False
    except:
        pass


def _hide_all(e):
    visible_popovers = _visible_popovers.copy()
    for (
        popover_id
    ) in visible_popovers:  # use copy since we don't want the dict to change size
        _hide(popover_id, visible_popovers)


_window.addEventListener("scroll", _hide_all, True)


def _is_visible(popper_element):
    return popper_element.attr("popover_id") in _visible_popovers


def _get_jquery_popper_element(popper):
    if isinstance(popper, _anvil.Button):
        # use the button node not the div node so that point is in the right place
        element = _anvil.js.get_dom_node(popper).firstElementChild
    else:
        element = _anvil.js.get_dom_node(popper)
    return _S(element)  # return the jquery element


def _hide_popovers_on_outside_click(e):
    target = e.target
    if target.classList.contains("anvil-popover"):
        nearest_id = target.getAttribute("popover_id")
    else:
        nearest_id = _S(target).closest(".anvil-popover").attr("popover_id")
    visible_popovers = _visible_popovers.copy()
    for (
        popover_id
    ) in visible_popovers:  # use copy since we don't want the dict to change size
        if nearest_id is not popover_id:
            _hide(popover_id, visible_popovers)


# make this the default behaviour
dismiss_on_outside_click(True)


def _get_random_string(_len):
    return "".join(_random_choice(_letters) for _ in range(_len))


_visible_popovers = {}

_template = '<div class="popover anvil-popover" role="tooltip" popover_id={} style="max-width:{}; "><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'

# temp style for updating popovers without transition animations
_S(
    """<style>
.PopNoTransition {
    -moz-transition: none !important;
    -webkit-transition: none !important;
    -o-transition: none !important;
    transition: none !important;
}
</style>
"""
).appendTo(_S("head"))


if __name__ == "__main__":
    _ = _anvil.ColumnPanel()
    _.set_event_handler(
        "show",
        lambda **e: _anvil.Notification(
            "oops, popover is a dependency", style="danger", timeout=None
        ).show(),
    )
    _anvil.open_form(_)

_ = None
