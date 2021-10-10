# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import Component as _Component
from anvil.js import await_promise as _await_promise
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import Function as _Function

__version__ = "1.7.1"

__all__ = ["animate", "animate_in", "animate_out", "wait_for", "Easing", "Transition"]


class Easing:
    def __new__(cls):
        raise TypeError("Easing is an enum class and shouldn't be instantiated")

    ease_in_out = "ease-in-out"
    ease_out = "ease-out"
    ease_in = "ease-in"
    ease = "ease"
    linear = "linear"

    @staticmethod
    def cubic_bezier(po, p1, p2, p3):
        return f"cubic-bezier({po}, {p1}, {p2}, {p3})"


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
        return transitions

    def __init__(
        self,
        *,
        transform=None,
        opacity=None,
        backgroundColor=None,
        offset=None,
        **transitions,
    ):
        # This is just for the autocomplete
        pass


_Function(
    """
window.Animation.prototype.wait = function() {
    return this.finished;
};
"""
)()


class Animation:
    # This class is only for the auto-completions
    def __new__(cls, animation):
        return animation

    def cancel(self) -> None:
        "abort animation playback"

    def commitStyles(self) -> None:
        "Commits the end styling state of an animation to the element"

    def finish(self) -> None:
        "Seeks the end of an animation"

    def play(self) -> None:
        "Starts or resumes playing of an animation, or begins the animation again if it previously finished."

    def persist(self) -> None:
        "Explicitly persists an animation, when it would otherwise be removed."

    def pause(self) -> None:
        "Suspends playing of an animation"

    def wait(self) -> None:
        "Animations are not blocking. Call the wait function to wait for an animation to finish in a blocking way"

    def reverse(self) -> None:
        "Reverses playback direction and plays"

    def updatePlaybackRate(self, playback_rate) -> None:
        "The new speed to set. A positive number (to speed up or slow down the animation), a negative number (to reverse), or zero (to pause)."

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


def _combine_options(
    options, duration, delay, direction, easing, endDelay, fill, iterations
):
    return options | {
        "duration": duration,
        "delay": delay,
        "direction": direction,
        "easing": easing,
        "endDelay": endDelay,
        "fill": fill,
        "iterations": iterations,
    }


def _animate(component, keyframes, options):
    element = _get_dom_node(component)
    return Animation(element.animate(keyframes, options))


def animate(
    component,
    transitions,
    *,
    duration=333,
    delay=0,
    direction="normal",
    easing="linear",
    endDelay=0,
    fill="none",
    iterations=1,
    **options,
):
    """a wrapper around the browser's Animation API. see MDN docs for full details
    component: an anvil component
    transitions: Transion object | dict | list - e.g. Transition(opacity=[0, 1])
    **options: various options to change the behaviour of the animation
    """
    options = _combine_options(
        options, duration, delay, direction, easing, endDelay, fill, iterations
    )
    return _animate(component, transitions, options)


def animate_in(
    component,
    transitions,
    *,
    duration=333,
    delay=0,
    direction="normal",
    easing="linear",
    endDelay=0,
    fill="none",
    iterations=1,
    **options,
):
    """equivalent to adding an animation to the show event of a component"""
    options = _combine_options(
        options, duration, delay, direction, easing, endDelay, fill, iterations
    )

    def on_show(**e):
        _animate(component, transitions, options)

    component.add_event_handler("show", on_show)


_out_animations = {}


def animate_out(
    component,
    transitions,
    *,
    duration=333,
    delay=0,
    direction="normal",
    easing="linear",
    endDelay=0,
    fill="none",
    iterations=1,
    **options,
):
    """animation to use when calling remove_from_parent"""
    options = _combine_options(
        options, duration, delay, direction, easing, endDelay, fill, iterations
    )
    _out_animations[component] = (transitions, options)


def wait_for(animation):
    """equivalent to animation.wait()"""
    _await_promise(animation.finished)


#### private override remove_from_parent to support animation exits
_old_remove = _Component.remove_from_parent


def _new_remove(self):
    out = _out_animations.get(self)
    if out is not None:
        _animate(self, *out).wait()
    return _old_remove(self)


_Component.remove_from_parent = _new_remove
