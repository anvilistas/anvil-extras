# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import Component as _Component
from anvil.js import await_promise as _await_promise
from anvil.js import get_dom_node as _get_dom_node
from anvil.js import window as _window

__version__ = "1.7.1"

__all__ = [
    "animate",
    "is_animating",
    "get_bounding_rect",
    "wait_for",
    "Easing",
    "Transition",
    "Effect",
]


class _Easing:
    def __init__(self):
        # really should be class variables
        # but anvil autocomplete prefers instance variables
        self.ease_in_out = "ease-in-out"
        self.ease_out = "ease-out"
        self.ease_in = "ease-in"
        self.ease = "ease"
        self.linear = "linear"

    def cubic_bezier(self, po, p1, p2, p3):
        return f"cubic-bezier({po}, {p1}, {p2}, {p3})"


Easing = _Easing()


class Transition(dict):
    # Some pre-styled transitions
    fly_out_below = {
        "transform": ["translateY(0) scale(1)", "translateY(100%) scale(0)"],
        "opacity": [1, 0],
    }
    fly_out_above = {
        "transform": ["translateY(0) scale(1)", "translateY(-100%) scale(0)"],
        "opacity": [1, 0],
    }
    fly_out_left = {
        "transform": ["translateX(0) scale(1)", "translateX(-100%) scale(0)"],
        "opacity": [1, 0],
    }
    fly_out_right = {
        "transform": ["translateX(0) scale(1)", "translateX(100%) scale(0)"],
        "opacity": [1, 0],
    }
    fly_in_below = {
        "transform": ["translateY(-100%) scale(0)", "translateY(0) scale(1)"],
        "opacity": [0, 1],
    }
    fly_in_above = {
        "transform": ["translateY(100%) scale(0)", "translateY(0) scale(1)"],
        "opacity": [0, 1],
    }
    fly_in_left = {
        "transform": ["translateX(100%) scale(0)", "translateX(0) scale(1)"],
        "opacity": [0, 1],
    }
    fly_in_right = {
        "transform": ["translateX(-100%) scale(0)", "translateX(0) scale(1)"],
        "opacity": [0, 1],
    }
    fade_out = {"opacity": [1, 0]}
    fade_in = {"opacity": [0, 1]}
    fade_in_slow = {"opacity": [0, 0.25, 1], "offset": [0, 0.75]}
    grow_shrink = {"transform": ["scale(1)", "scale(1.5)", "scale(1)"]}

    def __new__(cls, **transitions):
        # this really just returns the dictionary passed
        # if we wanted to we could do some type checking
        return transitions

    def __init__(
        self,
        *,
        transform=None,
        opacity=None,
        backgroundColor=None,
        offset=None,
        **css_transitions,
    ):
        # just for the autocomplete - some common css transitions included as kwargs
        pass


# add a method to the window.Animation class for our convenience
_window.Function(
    """
Animation.prototype.wait = function() {
    return this.finished;
};
"""
)()


class Animation:
    def __new__(cls, animation):
        # we just return the animation object
        # the only job of this class is to provide autocompletions
        return animation

    def cancel(self) -> None:
        "abort animation playback"

    def commitStyles(self) -> None:
        "Commits the end styling state of an animation to the element"

    def finish(self) -> None:
        "Seeks the end of an animation"

    def pause(self) -> None:
        "Suspends playing of an animation"

    def play(self) -> None:
        "Starts or resumes playing of an animation, or begins the animation again if it previously finished."

    def persist(self) -> None:
        "Explicitly persists an animation, when it would otherwise be removed."

    def reverse(self) -> None:
        "Reverses playback direction and plays"

    def updatePlaybackRate(self, playback_rate) -> None:
        "The new speed to set. A positive number (to speed up or slow down the animation), a negative number (to reverse), or zero (to pause)."

    def wait(self) -> None:
        "Animations are not blocking. Call the wait function to wait for an animation to finish in a blocking way"

    @property
    def playbackRate(self) -> int or float:
        "gets or sets the playback rate"

    @property
    def onfinish(self):
        "set a callback for when the animation finishes"

    @property
    def oncancel(self):
        "set a callback for when the animation is canceled"

    @property
    def onremove(self):
        "set a callback for when the animation is removed"


def _make_timing_options(
    duration,
    delay,
    direction,
    easing,
    endDelay,
    fill,
    iterations,
    iterationStart,
    composite,
):
    return {
        "duration": duration,
        "delay": delay,
        "direction": direction,
        "easing": easing,
        "endDelay": endDelay,
        "fill": fill,
        "iterations": iterations,
        "iterationStart": iterationStart,
        "composite": composite,
    }


def _dom_node(component):
    if isinstance(component, _Component):
        return _get_dom_node(component)
    elif hasattr(component, "nodeType"):
        return component
    raise TypeError(
        f"Expectd an anvil Component or HTMLElement (got {component.__class__.__name__})"
    )


def _animate(component, keyframes, options, use_ghost=False):
    el = _dom_node(component)

    if use_ghost:
        _animate_ghost(el, keyframes, options)

    return Animation(el.animate(keyframes, options))


def is_animating(component) -> bool:
    el = _dom_node(component)
    return any(a.playState == "running" for a in el.getAnimations())


def animate(
    component,
    transitions=None,
    *,
    duration=333,
    start_at=None,
    end_at=None,
    use_ghost=False,
    delay=0,
    direction="normal",
    easing="linear",
    endDelay=0,
    fill="none",
    iterations=1,
    iterationStart=0,
    composite="replace",
):
    """a wrapper around the browser's Animation API. see MDN docs for full details
    component: an anvil Component or js HTMLElement
    transitions: Transion object | dict | list - e.g. Transition(opacity=[0, 1])
    **options: various options to change the behaviour of the animation
    """
    options = _make_timing_options(
        duration,
        delay,
        direction,
        easing,
        endDelay,
        fill,
        iterations,
        iterationStart,
        composite,
    )
    if start_at is not None or end_at is not None:
        return _animate_from_to(
            component, start_at or component, end_at or component, transitions, options
        )
    return _animate(component, transitions, options, use_ghost)


def wait_for(animation_or_component):
    """can pass a component or an animation. Will wait for all animations running on the component to finish"""
    if hasattr(animation_or_component, "finished"):
        _await_promise(animation_or_component.finished)
        return
    el = _dom_node(animation_or_component)
    animations = el.getAnimations()
    _window.Promise.all(list(map(lambda a: a.finished, animations)))


def _animate_ghost(el, keyframes, options):
    ghost = el.cloneNode(True)
    pos = el.getBoundingClientRect(True)
    _window.Object.assign(
        ghost.style,
        {
            "position": "absolute",
            "left": f"{pos.x}px",
            "top": f"{pos.y}px",
            "width": f"{pos.width}px",
            "height": f"{pos.height}px",
            "margin": "0",
        },
    )
    _window.document.body.append(ghost)

    el.style.visible = "hidden"

    def ghost_finish(e):
        el.style.visible = "visible"
        ghost.remove()

    ghost.animate(keyframes, options).addEventListener("finish", ghost_finish)


def _animate_from_to(component, c1, c2, t, options):
    el = _dom_node(component)
    pos = el.getBoundingClientRect()
    pos1, pos2 = get_bounding_rect(c1), get_bounding_rect(c2)
    x1, x2 = pos1.x - pos.x, pos2.x - pos.x
    y1, y2 = pos1.y - pos.y, pos2.y - pos.y
    t_fromto = Transition(
        transform=[
            f"translateX({x1}px) translateY({y1}px)",
            f"translateX({x2}px) translateY({y2}px)",
        ]
    )
    if pos1.width != pos2.width:
        t_fromto["width"] = [pos1.width, pos2.width]
    if pos1.height != pos2.height:
        t_fromto["height"] = [pos1.height, pos2.height]

    t = (t or {}) | t_fromto

    # we create a ghost node
    _animate_ghost(el, t, options)
    return Animation(_animate(component, t, options))


class DOMRect:
    # For autocompletions only
    def __new__(cls, *, x=None, y=None, width=None, height=None, obj=None):
        if obj is not None:
            return obj
        else:
            return _window.DOMRect(x, y, width, height)

    def __init__(self, *, x, y, width, height):
        # another just for the autocomplete
        pass

    @property
    def x(self) -> int or float:
        "x position on the page"

    @property
    def y(self) -> int or float:
        "y position on the page"

    @property
    def height(self) -> int or float:
        pass

    @property
    def width(self) -> int or float:
        pass

    @property
    def left(self) -> int or float:
        "equivalent to x"

    @property
    def top(self) -> int or float:
        "equivalent to y"


def get_bounding_rect(component) -> DOMRect:
    """returns an object with attributes relating to the position of the component on the page: height, width, x, y"""
    if component.__class__ == _window.DOMRect:
        return component
    el = _dom_node(component)
    return DOMRect(obj=el.getBoundingClientRect())


_window.Function(
    "_animate",
    """
KeyframeEffect.prototype.animate = function(component, ghost=false) {
    const keyframes = this.getKeyframes();
    const timing = this.getTiming();
    return _animate(component, keyframes, timing, ghost);
}
""",
)(_animate)


class Effect:
    def __new__(cls, transitions=None, **timings):
        return _window.KeyframeEffect(None, transitions, timings)

    def __init__(
        self,
        transitions=None,
        *,
        duration=333,
        delay=0,
        direction="normal",
        easing="linear",
        endDelay=0,
        fill="none",
        iterations=1,
        iterationStart=0,
        composite="replace",
    ):
        pass

    def animate(self, component, use_ghost=False) -> Animation:
        "animate a component using an effect"
        return Animation(None)

    def getKeyframes(self, component):
        "Returns the computed keyframes that make up this effect"

    def getTiming(self, component):
        "The EffectTiming object associated with the animation"
