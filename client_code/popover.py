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

import anvil as _anvil
from anvil.js import window as _window
from anvil.js.window import Promise as _Promise
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S

__version__ = "1.8.1"

__all__ = ["popover", "pop", "dismiss_on_outside_click", "set_default_max_width"]


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
    component = None
    if isinstance(content, str):
        html = False
    elif isinstance(content, _anvil.Component):
        html = True
        content.popper = self  # add the popper to the content form
        component = content
        content = _anvil.js.get_dom_node(content)  # get the dom node
    else:
        type_name = type(content).__name__
        msg = "content to a popover should be either a str or anvil Component, not {}"
        raise TypeError(msg.format(type_name))

    popper_element = _get_jquery_popper_element(self)
    # We could be in the middle of a 'destroy'
    _wait_for_transition(popper_element)

    if _has_popover(popper_element):
        msg = (
            "Warning: attempted to create a popover on a component that already has one. This will have no effect.\n"
            "Destroy the popover before creating a new one using component.pop('destroy').\n"
            "Or, use has_popover() to check if this component aleady has a popover."
        )
        print(msg)
        # return here since adding a new popover has no effect
        return

    popper_id = _get_next_id()
    max_width = _default_max_width if max_width is None else max_width

    _add_transition_behaviour(component, popper_element, popper_id)

    if trigger == "stickyhover":
        trigger = "manual"
        _add_sticky_behaviour(self, popper_element, popper_id)

    # can effect the title of the popover so temporarily set it to ''
    tooltip = getattr(self, "tooltip", None)
    if tooltip:
        self.tooltip = ""

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

    popper_element.addClass("anvil-popover")
    popper_element.attr("popover_id", popper_id)
    popper_element.data(
        "ae.popover",
        {
            "autoDismiss": bool(auto_dismiss),
            "inTransition": None,
        },
    )


def pop(self, behavior):
    """behaviour can be any of
    show, hide, toggle, destroy (included with bootstrap 3.4.1)

    features added not in bootstrap 3.4.1 docs:
    update  - updates position of popover - useful for dynamic content that changes the size of the popover
    shown: returns True or False if the popover is visible - note a popover will only be visible after it has animated onto screen so may need to sleep(.15) before calling
    is_visible: same as shown
    """
    popper_element = _get_jquery_popper_element(self)
    _wait_for_transition(popper_element)

    if behavior == "shown" or behavior == "is_visible":
        return _is_visible(popper_element)
    elif behavior == "update":
        return _update_positions()

    _popper_execute(popper_element, behavior)


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


def has_popover(component):
    if not isinstance(component, _anvil.Component):
        raise TypeError("Expected a component, not " + type(component).__name__)
    popper_element = _get_jquery_popper_element(component)
    _wait_for_transition(popper_element)
    # just incase we're being destroyed
    return _has_popover(popper_element)


_anvil.Component.popover = popover
_anvil.Component.pop = pop

######## helper functions ########

_popper_count = 0


def _get_next_id():
    global _popper_count
    _popper_count += 1
    return str(_popper_count)


def _get_data(popper_element, attr, default=None):
    data = popper_element.data("ae.popover")
    if data is not None:
        return data.get(attr, default)
    return default


def _set_data(popper_element, attr, value):
    data = popper_element.data("ae.popover")
    if data is not None:
        data[attr] = value


def _add_transition_behaviour(component, popper_element, popper_id):
    # clean up our previous event handlers
    popper_element.off(
        "show.bs.popover shown.bs.popover hide.bs.popover hidden.bs.popover"
    )

    # transition is either None or a promise
    fake_container = _anvil.Container()

    def resolve_shown(resolve, _reject):
        def f(e):
            _set_data(popper_element, "inTransition", None)
            popper_element.off("shown.bs.popover", f)
            resolve(None)
            open_form = _anvil.get_open_form()
            if open_form is not None and fake_container.parent is None:
                open_form.add_component(fake_container)
            if component is None:
                return
            elif component.parent is None:
                # we add the component to a Container component
                # this doesn't really add it to the dom
                # it just allows us to use anvil's underlying show hide architecture
                fake_container.add_component(component)
            elif type(component.parent) is _anvil.Container:
                pass  # just ignore this - it's probably something internal
            else:
                print(
                    "Warning: the popover content already has a parent this can cause strange behaviour"
                )

        popper_element.on("shown.bs.popover", f)

    def show_in_transition(e):
        _set_data(popper_element, "inTransition", _Promise(resolve_shown))
        _visible_popovers[popper_id] = popper_element

    popper_element.on("show.bs.popover", show_in_transition)

    def resolve_hidden(resolve, _reject):
        def f(e):
            _visible_popovers.pop(popper_id, None)
            _set_data(popper_element, "inTransition", None)
            if component is not None and component.parent is fake_container:
                component.remove_from_parent()
            fake_container.remove_from_parent()
            popper_element.off("hidden.bs.popover", f)
            resolve(None)

        popper_element.on("hidden.bs.popover", f)

    def hide_in_transition(e):
        _set_data(popper_element, "inTransition", _Promise(resolve_hidden))

    popper_element.on("hide.bs.popover", hide_in_transition)


def _wait_for_transition(popper_element):
    transition = _get_data(popper_element, "inTransition")
    if transition is not None:
        _anvil.js.await_promise(transition)


_sticky_popovers = set()


def _add_sticky_behaviour(self, popper_element, popper_id):
    from time import sleep

    def sticky_leave(e):
        sleep(0.1)  # small delay to allow the mouse to move to the element
        if not _S("[popover_id='{}']:hover".format(popper_id)):
            pop(self, "hide")

    def sticky_enter(e):
        if not pop(self, "is_visible"):
            pop(self, "show")

    popper_element.on("mouseenter", sticky_enter).on("mouseleave", sticky_leave)
    _set_sticky_hover()
    _sticky_popovers.add(popper_id)


def _sticky_leave(e):
    popper_element = None
    popover_id = _S(e.currentTarget).attr("popover_id")
    if popover_id in _sticky_popovers and not _S(
        "[popover_id='{}']:hover".format(popover_id)
    ):
        popper_element = _visible_popovers.get(popover_id)
    if popper_element is not None:
        _popper_execute(popper_element, "hide")


def _set_sticky_hover():
    if not _sticky_popovers:
        _S("body").on("mouseleave", ".popover", _sticky_leave)


def _update_positions(*args):
    if _scrolling:
        # not sure why this fires on scroll but it does on chrome
        return
    _S(".popover").addClass("PopNoTransition").popover("show").removeClass(
        "PopNoTransition"
    )


_window.addEventListener("resize", _update_positions)


_scrolling = False


def _hide_on_scroll(e):
    global _scrolling
    if (
        _scrolling
        or not _visible_popovers
        or e.target.closest(".anvil-popover") is not None
    ):
        return

    _scrolling = True

    def do_hide(*args):
        global _scrolling
        transitions = []
        try:
            for popper_element in _visible_popovers.copy().values():
                _popper_execute(popper_element, "hide")
                transitions.append(_get_data(popper_element, "inTransition"))
            _anvil.js.await_promise(_Promise.all(transitions))
        finally:
            _scrolling = False

    _window.requestAnimationFrame(do_hide)


_window.addEventListener("scroll", _hide_on_scroll, True)


def _popper_execute(popper_element, behavior: str):
    # see bug https://github.com/twbs/bootstrap/issues/16732
    if behavior not in ("hide", "show", "toggle", "destroy"):
        raise ValueError("unrecognized behavior: {}".format(behavior))

    if not _has_popover(popper_element):
        return

    if behavior == "hide":
        popper_element.data("bs.popover").inState.click = False
    elif behavior == "show":
        popper_element.data("bs.popover").inState.click = True
    elif behavior == "toggle":
        current = popper_element.data("bs.popover").inState.click
        popper_element.data("bs.popover").inState.click = not current

    popper_element.popover(behavior)


def _is_visible(popper_element):
    return popper_element.attr("popover_id") in _visible_popovers


def _has_popover(popper_element):
    return popper_element.data("bs.popover") is not None


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
    # use copy since the dict changes size during iteration
    for popover_id, popper_element in _visible_popovers.copy().items():
        if nearest_id == popover_id:
            continue
        if _get_data(popper_element, "autoDismiss", True):
            _popper_execute(popper_element, "hide")


# make this the default behaviour
dismiss_on_outside_click(True)

_visible_popovers = {}

_template = '<div class="popover anvil-popover" role="tooltip" popover_id="{}" style="max-width:{};"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'

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
