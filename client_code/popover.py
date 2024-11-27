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
import anvil.js
from anvil.js.window import WeakMap as _WeakMap
from anvil.js.window import document as _document
from anvil.js.window import window as _W

from . import fui
from .utils._component_helpers import _html_injector
from .utils._component_helpers import walk as _walk
from .utils._deprecated import deprecated as _deprecated
from .utils._warnings import warn as _warn

__version__ = "3.0.0"

__all__ = [
    "popover",
    "pop",
    "dismiss_on_outside_click",
    "dismiss_on_scroll",
    "set_default_max_width",
    "set_default_container",
]

_popper_map = _WeakMap()
_visible_popovers = {}


css = """
.ae-popover {
    z-index: 1060;
    max-width: 276px;
    padding: 1px;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: 400;
    line-height: 1.42857143;
    line-break: auto;
    text-align: start;
    text-decoration: none;
    text-shadow: none;
    text-transform: none;
    letter-spacing: normal;
    word-break: normal;
    word-spacing: normal;
    word-wrap: normal;
    white-space: normal;
    font-size: 14px;
    background-color: var(--ae-popover-bg, #fff);
    background-clip: padding-box;
    border: 1px solid var(--ae-popover-border, rgba(0, 0, 0, 0.2));
    border-radius: 6px;
    box-shadow: var(--ae-popover-shadow, 0 5px 10px var(--ae-popover-border, rgba(0, 0, 0, 0.2)));
    display: flex;
}
.ae-popover-container {
    display: flex;
    flex-direction: column;
}
.ae-popover-title {
    padding: 8px 14px;
    margin: 0;
    font-size: 14px;
    background-color: var(--ae-popover-title-bg, #f7f7f7);
    border-bottom: 1px solid var(--ae-popover-title-border, #ebebeb);
    border-radius: 5px 5px 0 0;
}
.ae-popover-content {
    padding: 9px 14px;
    min-height: 0;
}
.ae-popover-container > .ae-arrow {
    border-width: 11px;
}
.ae-popover-container > .ae-arrow, .ae-popover-container > .ae-arrow:after {
    position: absolute;
    display: block;
    width: 0;
    height: 0;
    border-color: transparent;
    border-style: solid;
}
.ae-popover.left > .ae-popover-container > .ae-arrow {
    border-right-width: 0;
    border-left-color: var(--ae-popover-border, rgba(0, 0, 0, 0.2));
}
.ae-popover.right > .ae-popover-container > .ae-arrow {
    border-right-color: var(--ae-popover-border, rgba(0, 0, 0, 0.2));
    border-left-width: 0;
}
.ae-popover.bottom > .ae-popover-container > .ae-arrow {
    border-top-width: 0;
    border-bottom-color: var(--ae-popover-border, rgba(0, 0, 0, 0.2));
}
.ae-popover.top > .ae-popover-container > .ae-arrow {
    border-top-color: var(--ae-popover-border, rgba(0, 0, 0, 0.2));
    border-bottom-width: 0;
}

.ae-popover > .ae-popover-container > .ae-arrow:after {
    content: "";
    border-width: 10px;
}
.ae-popover.right > .ae-popover-container > .ae-arrow:after {
    bottom: -10px;
    left: 1px;
    content: " ";
    border-right-color: var(--ae-popover-bg, #fff);
    border-left-width: 0;
}
.ae-popover.left > .ae-popover-container > .ae-arrow:after {
    right: 1px;
    bottom: -10px;
    content: " ";
    border-right-width: 0;
    border-left-color: var(--ae-popover-bg, #fff);
}
.ae-popover.top > .ae-popover-container > .ae-arrow:after {
    bottom: 1px;
    margin-left: -10px;
    content: " ";
    border-top-color: var(--ae-popover-bg, #fff);
    border-bottom-width: 0;
}
.ae-popover.bottom >  .ae-popover-container > .ae-arrow:after {
    top: 1px;
    margin-left: -10px;
    content: " ";
    border-top-width: 0;
    border-bottom-color: var(--ae-popover-bg, #fff);
}
"""

_html_injector.css(css)


class _State:
    visible = "visible"
    hidden = "hidden"


def _noop():
    pass


def _get_popper_element(component):
    if not isinstance(component, _anvil.Component):
        raise TypeError(f"invalid component, got {type(component).__name__}")

    dom_node = _anvil.js.get_dom_node(component)
    if isinstance(component, _anvil.Button):
        return dom_node.firstElementChild

    return dom_node


def _is_on_screen(component):
    open_form = _anvil.get_open_form()
    if open_form is None:
        return False

    parent = component
    while parent is not None:
        if parent is open_form:
            return True
        parent = parent.parent

    return False


def _get_root():
    f = _anvil.get_open_form()
    while isinstance(f, _anvil.WithLayout):
        f = f.layout

    return f


_VALID_MAIN = ("top", "right", "bottom", "left", "bottom")
_VALID_SECONDARY = ("", "-start", "-end")
_VALID_PLACEMENTS = tuple(
    f"{main}{secondary}" for main in _VALID_MAIN for secondary in _VALID_SECONDARY
)
_VALID_TRIGGERS = ("click", "hover", "focus", "stickyhover")


class Popover:
    _id = 0
    _has_sticky = 0

    @classmethod
    def get_next_id(cls):
        cls._id += 1
        return cls._id

    def __init__(
        self,
        popper,
        poppee,
        title="",
        placement="right",
        trigger="click",
        animation=True,
        delay=None,
        max_width=None,
        auto_dismiss=True,
        dismiss_on_scroll=None,
        container=None,
        arrow=True,
    ):
        _popper_map.set(popper, self)

        self.id = self.get_next_id()
        self.state = _State.hidden

        self.popper = popper
        self.poppee = poppee

        self.title = title
        self.arrow = arrow

        if not isinstance(placement, str):
            raise TypeError("placement must be a string")

        if placement in _VALID_PLACEMENTS:
            self.placement = placement
        else:
            placements = placement.strip().lower().split(" ")
            self.placement = next(
                (p for p in placements if p in _VALID_PLACEMENTS), "right"
            )

        if not isinstance(trigger, str):
            raise TypeError("trigger must be a string")

        if trigger in _VALID_TRIGGERS:
            self.triggers = [trigger]
        else:
            self.triggers = trigger.strip().lower().split(" ")
            if "manual" in self.triggers:
                self.triggers = ["manual"]

        self.animation_ms = 150 if animation else 0

        if isinstance(delay, (int, float)):
            self.delay = {"show": delay, "hide": delay}
        elif isinstance(delay, dict):
            self.delay = {"show": 100, "hide": 100} | delay
        elif delay is None:
            self.delay = {"show": 100, "hide": 100}
        else:
            raise TypeError("delay must be an int, float, dict or None")

        self.max_width = _default_max_width if max_width is None else max_width
        self.container = _default_container if container is None else container

        self.auto_dismiss = auto_dismiss

        self.timeouts = []
        self.cleanup = _noop

        # we use this to allow show-hide events to be fired on the content
        self.fake_container = _anvil.Container()
        self._clicked = False

        if dismiss_on_scroll is not None:
            _warn(
                "popover.dismiss_on_scroll",
                "dismiss_on_scroll option is deprecated",
                "DEPRECATION WARNING",
            )

        self.make_template()
        self.add_behavior()

    def make_template(self):
        d = _document.createElement("div")
        d.className = "ae-popover"
        d.style.position = "absolute"
        d.style.visibility = "hidden"
        d.style.opacity = "0"
        d.style.maxWidth = self.max_width
        ms = self.animation_ms
        if ms:
            d.style.transition = f"opacity {ms}ms linear, visibility {ms}ms linear"
        self.init_popover(d)
        d.role = "tooltip"

        c = _document.createElement("div")
        c.className = "ae-popover-container"
        d.append(c)

        arrow = _document.createElement("div")
        if self.arrow:
            c.append(arrow)
            arrow.className = "ae-arrow"

        title = _document.createElement("div")
        c.append(title)
        if self.title:
            title.textContent = self.title
        else:
            title.style.display = "none"
        title.className = "ae-popover-title"

        content = _document.createElement("div")
        c.append(content)
        content.className = "ae-popover-content"

        self.dom_popover = d
        self.dom_content = content
        self.dom_arrow = arrow

    def init_popover(self, element):
        element = _anvil.js.get_dom_node(element)
        element.setAttribute("ae-popover", "")
        element.setAttribute("ae-popover-id", self.id)

    def cleanup_popover(self, element):
        try:
            element = _anvil.js.get_dom_node(element)
        except TypeError:
            pass
        element.removeAttribute("ae-popover")
        element.removeAttribute("ae-popover-id")

    def add_behavior(self):
        self.popper.add_event_handler("x-anvil-page-shown", self.handle_mount)
        self.popper.add_event_handler("x-anvil-page-hidden", self.handle_cleanup)
        if _is_on_screen(self.popper):
            self.handle_mount()

    def handle_mount(self, **e):
        el = _get_popper_element(self.popper)
        if "click" in self.triggers:
            el.addEventListener("click", self.toggle, True)
        if "hover" in self.triggers:
            el.addEventListener("mouseenter", self.show, True)
            el.addEventListener("mouseleave", self.hide, True)
        if "focus" in self.triggers:
            el.addEventListener("focus", self.show, True)
            el.addEventListener("blur", self.hide, True)
        if "stickyhover" in self.triggers:
            if not Popover._has_sticky:
                _document.body.addEventListener(
                    "mouseleave", self.document_sticky_mouseleave_handler, True
                )

            Popover._has_sticky += 1
            el.addEventListener("mouseenter", self.show, True)
            el.addEventListener("mouseleave", self.sticky_hide, True)

    def handle_cleanup(self, **e):
        el = _get_popper_element(self.popper)
        if "click" in self.triggers:
            el.removeEventListener("click", self.toggle, True)
        if "hover" in self.triggers:
            el.removeEventListener("mouseenter", self.show, True)
            el.removeEventListener("mouseleave", self.hide, True)
        if "focus" in self.triggers:
            el.removeEventListener("focus", self.show, True)
            el.removeEventListener("blur", self.hide, True)
        if "stickyhover" in self.triggers:
            Popover._has_sticky -= 1
            if not Popover._has_sticky:
                _document.body.removeEventListener(
                    "mouseleave", self.document_sticky_mouseleave_handler, True
                )

            el.removeEventListener("mouseenter", self.show, True)
            el.removeEventListener("mouseleave", self.sticky_hide, True)

    @staticmethod
    def document_sticky_mouseleave_handler(e):
        # did we leave a popover?
        target = _clean_target(e.target)
        if not (target and target.hasAttribute("ae-popover")):
            return

        popover_id = int(target.getAttribute("ae-popover-id"))

        # are we still hovering over the same popover?
        if _document.querySelector(f"[ae-popover-id='{popover_id}']:hover"):
            return

        popper = _visible_popovers.get(popover_id)
        if popper is None:
            return

        popover = _popper_map.get(popper)
        if popover is not None:
            popover.sticky_hide(e)

    def sticky_hide(self, *e):
        from time import sleep

        sleep(0.1)  # small delay to allow the mouse to move to the element
        if not _document.querySelector(f"[ae-popover-id='{self.id}']:hover"):
            self.hide(*e)

    def clear_timeouts(self):
        for timeout in self.timeouts:
            _W.clearTimeout(timeout)
        self.timeouts = []

    def animate(self, show=True):
        self.dom_popover.style.visibility = "visible" if show else "hidden"
        self.dom_popover.style.opacity = 1 if show else 0

    def animate_in(self):
        self.animate(True)

    def animate_out(self):
        self.animate(False)

    def setup_dom(self):
        if self.fake_container.parent is None:
            root = _get_root()
            if root is not None:
                root.add_component(self.fake_container)

        if self.poppee.parent is None:
            self.fake_container.add_component(self.poppee)

        if self.dom_content.firstChild is None:
            self.dom_content.append(_anvil.js.get_dom_node(self.poppee))

        el = _get_popper_element(self.popper)
        self.init_popover(el)

        for c in _walk(self.poppee):
            c.raise_event("x-popover-init", init_node=self.init_popover)

        if self.dom_popover.isConnected:
            return

        container = self.container
        if container == "body":
            container = _document.body
        elif isinstance(container, str):
            container = _document.querySelector(container)
            if container is None:
                container = _document.body
        try:
            container.append(self.dom_popover)
        except AttributeError:
            _document.body.append(self.dom_popover)

    def cleanup_dom(self):
        self.dom_popover.remove()
        self.poppee.remove_from_parent()
        self.fake_container.remove_from_parent()
        el = _get_popper_element(self.popper)
        self.cleanup_popover(el)

        for c in _walk(self.poppee):
            c.raise_event("x-popover-destroy", init_node=self.cleanup_popover)

    def on_shown(self):
        pass

    def show(self, *e):
        # exit early if we're already showing
        is_hover = e and e[0].type == "mouseenter"
        if not is_hover:
            self._clicked = True

        if self.state == _State.visible:
            return

        self.state = _State.visible
        _visible_popovers[self.id] = self.popper

        self.cleanup()
        self.setup_dom()

        self.clear_timeouts()

        self.dom_popover.style.display = ""

        self.cleanup = fui.auto_update(
            _get_popper_element(self.popper),
            self.dom_popover,
            placement=self.placement,
            arrow=self.dom_arrow if self.arrow else None,
        )

        delay = self.delay["show"] if e else 0
        self.timeouts.append(_W.setTimeout(self.animate_in, delay))
        self.timeouts.append(_W.setTimeout(self.on_shown, delay + self.animation_ms))
        self.poppee.raise_event("x-popover-show")

    def on_hidden(self):
        self.dom_popover.style.display = "none"
        self.cleanup()
        self.cleanup = _noop
        self.cleanup_dom()

    def hide(self, *e):
        is_hover = e and e[0].type == "mouseleave"

        if not is_hover:
            self._clicked = False

        if self.state == _State.hidden:
            return

        if is_hover and self._clicked:
            return

        self.state = _State.hidden
        _visible_popovers.pop(self.id, None)

        self.clear_timeouts()

        delay = self.delay["hide"] if e else 0
        self.timeouts.append(_W.setTimeout(self.animate_out, delay))
        self.timeouts.append(_W.setTimeout(self.on_hidden, delay + self.animation_ms))
        self.poppee.raise_event("x-popover-hide")

    def shown(self):
        return self.state == _State.visible

    def toggle(self, *e):
        if self.state == _State.visible:
            self.hide(*e)
        else:
            self.show(*e)

    def destroy(self):
        # remove all event listeners
        self.clear_timeouts()
        try:
            self.popper.remove_event_handler("x-anvil-page-shown", self.handle_mount)
            self.popper.remove_event_handler("x-anvil-page-hidden", self.handle_cleanup)
        except Exception:
            pass

        if _is_on_screen(self.popper):
            self.handle_cleanup()

        # remove us from the popper map
        _popper_map.delete(self.popper)
        _visible_popovers.pop(self.id, None)
        self.on_hidden()

    def is_visible(self):
        return self.shown()

    def update(self):
        # no longer does anything since we are using autoUpdate
        pass


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
    dismiss_on_scroll=None,
    container=None,
    arrow=True,
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
    if _popper_map.has(self):
        _warn(
            "popover.has_pop",
            "attempted to create a popover on a component that already has one. This will have no effect.\n"
            "Destroy the popover before creating a new one using component.pop('destroy').\n"
            "Or, use has_popover() to check if this component aleady has a popover before creating a new one.",
        )
        return

    if isinstance(content, str):
        content = _anvil.Label(text=content)
    if isinstance(content, _anvil.Component):
        try:
            content.popper = self  # add the popper to the content form
        except AttributeError:
            pass
    else:
        raise TypeError(
            f"content to a popover should be either a str or anvil Component, not {type(content).__name__}"
        )

    parent = content.parent
    if parent is not None and type(parent) is not _anvil.Container:
        _warn(
            "popover.has_parent",
            "the popover content already has a parent this can cause unusual behaviour.\n"
            "Support for this may be removed in a future version.",
        )

    Popover(
        self,
        content,
        title=title,
        placement=placement,
        trigger=trigger,
        animation=animation,
        delay=delay,
        max_width=max_width,
        auto_dismiss=auto_dismiss,
        dismiss_on_scroll=dismiss_on_scroll,
        container=container,
        arrow=arrow,
    )


def pop(self, behavior):
    """behaviour can be any of
    show, hide, toggle, destroy (included with bootstrap 3.4.1)

    features added not in bootstrap 3.4.1 docs:
    update  - updates position of popover - useful for dynamic content that changes the size of the popover
    shown: returns True or False if the popover is visible - note a popover will only be visible after it has animated onto screen so may need to sleep(.15) before calling
    is_visible: same as shown
    """
    popover = _popper_map.get(self)
    if not popover:
        return

    execute = getattr(popover, behavior, _noop)
    return execute()


def get_all_parent_popover_ids(target):
    parent_ids = []
    current_element = target

    while current_element and current_element.tagName.lower() != "body":
        if current_element.hasAttribute("ae-popover-id"):
            try:
                popover_id = int(current_element.getAttribute("ae-popover-id"))
                parent_ids.append(popover_id)
            except (ValueError, TypeError):
                # Skip if the attribute is not a valid integer
                pass
        current_element = current_element.parentElement

    return parent_ids


def _clean_target(target):
    """ensure we are dealing with a dom element and not a node"""
    if not target:
        return None
    if target.nodeType != 1:
        target = target.parentElement
    return target


def _hide_popovers_on_outside_click(e):
    target = _clean_target(e.target)
    parent_ids = get_all_parent_popover_ids(target)

    # Use a copy since the dict changes size during iteration
    for popover_id, popper in _visible_popovers.copy().items():
        if popover_id in parent_ids:
            # Skip hiding popovers that are parents of the clicked element
            continue

        popover = _popper_map.get(popper)
        if not popover:
            continue

        if popover.auto_dismiss:
            popover.hide()


# this is the default behavior
def dismiss_on_outside_click(dismiss=True):
    """hide popovers when a user clicks outside the popover
    this is the default behavior
    """
    _document.body.removeEventListener("click", _hide_popovers_on_outside_click, True)
    if dismiss:
        _document.body.addEventListener("click", _hide_popovers_on_outside_click, True)


@_deprecated("dismiss_on_scroll is deprecated")
def dismiss_on_scroll(dismiss=True):
    """Deprecated."""
    pass


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


def has_popover(self):
    return _popper_map.has(self)


_anvil.Component.popover = popover
_anvil.Component.pop = pop


# make this the default behaviour
dismiss_on_outside_click(True)
