# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
#
#
# for more information visit the w3 bootstrap popover page
# https://www.w3schools.com/bootstrap4/bootstrap_ref_js_popover.asp
#
# or the bootstrap popover page for v 3.4.1
# https://getbootstrap.com/docs/3.4/javascript/#popovers
#

from random import choice as _random_choice
from string import ascii_letters as _letters

import anvil as _anvil
import anvil.js
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S
from anvil.js.window import window as _window

__version__ = "1.6.0"


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
    if isinstance(content, str):
        html = False
    elif isinstance(content, _anvil.Component):
        html = True
        content.popper = self  # add the popper to the content form
        content = _anvil.js.get_dom_node(content)  # get the dom node
    else:
        raise TypeError(
            "content to a popover should be either a str or anvil Component, not {}".format(
                type(content).__name__
            )
        )

    max_width = _default_max_width if max_width is None else max_width

    # can effect the title of the popover so temporarily set it to ''
    tooltip, self.tooltip = self.tooltip, ""

    popper_id = _get_random_string(5)
    popper_element = _get_jquery_popper_element(self)

    has_popover = popper_element.data("bs.popover") is not None
    if has_popover and self._in_transition:
        # we've been created and we're part way through a transition
        # wait for it to finish
        anvil.js.await_promise(self._in_transition)
    if has_popover:
        # clean up our previous event handlers
        popper_element.off("show.bs.popover")
        popper_element.off("shown.bs.popover")
        popper_element.off("hide.bs.popover")
        popper_element.off("hidden.bs.popover")

    # transition is either None or a promise
    self._in_transition = None

    def resolve_shown(resolve, _reject):
        def f(e):
            resolve(None)
            self._in_transition = None
            popper_element.off("shown.bs.popover", f)

        popper_element.on("shown.bs.popover", f)

    def show_in_transition(e):
        self._in_transition = _window.Promise(resolve_shown)

    popper_element.on("show.bs.popover", show_in_transition)

    def resolve_hidden(resolve, _reject):
        def f(e):
            resolve(None)
            self._in_transition = None
            popper_element.off("hidden.bs.popover", f)

        popper_element.on("hidden.bs.popover", f)

    def hide_in_transition(e):
        self._in_transition = _window.Promise(resolve_hidden)

    popper_element.on("hide.bs.popover", hide_in_transition)

    if trigger == "stickyhover":
        trigger = "manual"
        from time import sleep

        def sticky_leave(e):
            sleep(0.1)  # small delay to allow the mouse to move to the element
            if not _S("[popover_id={}]:hover".format(popper_id)):
                pop(self, "hide")

        popper_element.on(
            "mouseenter",
            lambda e: None if pop(self, "is_visible") else pop(self, "show"),
        ).on(
            "mouseleave",
            sticky_leave,
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
            "sanitize": False,
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
    if self._in_transition is not None:
        anvil.js.await_promise(self._in_transition)
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
    except Exception:
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
    except Exception:
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
