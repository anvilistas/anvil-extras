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

from time import sleep

import anvil as _anvil
from anvil.js import window as _window
from anvil.js.window import Promise as _Promise
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S

from .utils._component_helpers import walk as _walk

__version__ = "2.2.3"

__all__ = [
    "popover",
    "pop",
    "dismiss_on_outside_click",
    "dismiss_on_scroll",
    "set_default_max_width",
    "set_default_container",
]


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
    dismiss_on_scroll=True,
    container=None,
):
    """should be called by a button or link
    content - either text or an anvil component or Form
    placement -  right, left, top, bottom, auto (for left/right best to have links and buttons inside flow panels)
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

    has_popover = _has_popover(popper_element)
    _check_warnings(has_popover, component)
    if has_popover:
        # return here since adding a new popover has no effect
        return

    popper_id = _get_next_id()
    max_width = _default_max_width if max_width is None else max_width
    container = _default_container if container is None else container

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
            "container": container,
            "sanitize": False,
        }
    )

    if tooltip:
        self.tooltip = tooltip
        # otherwise the tooltip doesn't work for Buttons
        popper_element.attr("title", tooltip)

    make_popover = _popover_maker(popper_id)
    make_popover(popper_element)
    popper_element.data(
        "ae.popover",
        {
            "autoDismiss": bool(auto_dismiss),
            "autoScrollHide": bool(dismiss_on_scroll),
            "inTransition": None,
        },
    )

    if component is not None:
        for c in _walk(component):
            c.raise_event("x-popover-init", init_node=make_popover)


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
    _document.body.removeEventListener("click", _hide_popovers_on_outside_click, True)
    if dismiss:
        _document.body.addEventListener("click", _hide_popovers_on_outside_click, True)


# this is the default behavior
def dismiss_on_scroll(dismiss=True):
    """hide popovers when a user scrolls. This is the default behavior
    You should change the default container if you set this globally to False.
    """
    _window.removeEventListener("scroll", _hide_on_scroll, True)
    if dismiss:
        _window.addEventListener("scroll", _hide_on_scroll, True)


_default_max_width = ""


def set_default_max_width(width):
    """update the default max width - this is 276px by default - useful for wider components"""
    global _default_width
    _default_width = width


_default_container = "body"


def set_default_container(selector_or_element):
    """The default container for popovers is the body page.
    In advanced set ups when the popovers can scroll with the element, you will want to change this.
    This can also be set per popover"""
    global _default_container
    _default_container = selector_or_element


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


def _popover_maker(id):
    def _make_popover_element(dom_node):
        _S(dom_node).addClass("anvil-popover").attr("popover_id", id)

    return _make_popover_element


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


_warnings = {}


def _check_warnings(has_popover, component):
    if has_popover and not _warnings.get("has_pop"):
        msg = (
            "Warning: attempted to create a popover on a component that already has one. This will have no effect.\n"
            "Destroy the popover before creating a new one using component.pop('destroy').\n"
            "Or, use has_popover() to check if this component aleady has a popover before creating a new one."
        )
        print(msg)
        _warnings["has_pop"] = True
    elif (
        component is not None
        and component.parent is not None
        and type(component.parent) is not _anvil.Container
        and not _warnings.get("has_parent")
    ):
        # if the parent is an anvil Container then it's probably an internal issue
        print(
            "Warning: the popover content already has a parent this can cause unusual behaviour.\n"
            "Support for this may be removed in a future version."
        )
        _warnings["has_parent"] = True


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

        popper_element.on("shown.bs.popover", f)

    def fire_show_event(e):
        if component is None:
            return
        open_form = _anvil.get_open_form()
        if open_form is not None and fake_container.parent is None:
            open_form.add_component(fake_container)
        if component.parent is None:
            # we add the component to a Container component
            # this doesn't really add it to the dom
            # it just allows us to use anvil's underlying show hide architecture
            fake_container.add_component(component)

    popper_element.on("inserted.bs.popover", fire_show_event)

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
    bs_data = popper_element.data("bs.popover")
    if bs_data is None:
        return

    transition = _get_data(popper_element, "inTransition")
    if transition is not None:
        _anvil.js.await_promise(transition)
        return

    timeout = bs_data.get("timeout")
    # bs sets a timeout when it does a toggle with a delay
    if timeout is None:
        return

    delay = None
    hoverState = bs_data.get("hoverState")
    if hoverState == "in":
        delay = bs_data.options.delay.show
    elif hoverState == "out":
        delay = bs_data.options.delay.hide

    if delay is not None:
        sleep(delay / 1000)
        _wait_for_transition(popper_element)


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
        or (e.target is not _document and e.target.closest(".anvil-popover"))
    ):
        return

    _scrolling = True

    def do_hide(*args):
        global _scrolling
        transitions = []
        try:
            for popper_element in _visible_popovers.copy().values():
                if _get_data(popper_element, "autoScrollHide", True):
                    _popper_execute(popper_element, "hide")
                    transitions.append(_get_data(popper_element, "inTransition"))
            _anvil.js.await_promise(_Promise.all(transitions))
        finally:
            _scrolling = False

    _window.requestAnimationFrame(do_hide)


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
dismiss_on_scroll(True)

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
