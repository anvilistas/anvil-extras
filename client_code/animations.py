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


def _dom_node(component):
    # TODO remove this function when js.get_dom_node does the same thing
    if isinstance(component, _Component):
        return _get_dom_node(component)
    elif hasattr(component, "nodeType"):
        return component
    raise TypeError(
        f"Expectd an anvil Component or HTMLElement (got {component.__class__.__name__})"
    )


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
        """creates a cubic-bezier easing value from 4 numerical values"""
        return f"cubic-bezier({po}, {p1}, {p2}, {p3})"


Easing = _Easing()


class Transition(dict):
    """Create a transtion object. Takes property names as keyword arguments and each value should be a list of transitions for that property
    e.g. fly_right = Transition(transform=['none', 'translateX(100%) scale(0)'])

    Each list item represents css values to be applied across the transition.
    Typically the first value is the start of the transition and the last value is the end.
    Lists can be more than 2 values in which case the transition will be split across the values evenly.
    You can customize the even split by setting an offset which has values from 0, 1

    e.g. fade_in_slow = Transition(opacity=[0, 0.25, 1], offset=[0, 0.75, 1])

    Transition objects can be combined with the | operator (which behaves like merging dictionaries)
    e.g. t = fly_right | fade_out | Transtion(height=[f"{current_height}px", "0px"])
    """

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

    @classmethod
    def _h_w_out(cls, component, attr, out=True):
        hw = get_bounding_rect(component)[attr]
        return cls(height=[f"{hw}px", 0] if out else [0, f"{hw}px"])

    @classmethod
    def height_out(cls, component):
        return cls._h_w_out(component, "height", True)

    @classmethod
    def width_out(cls, component):
        return cls._h_w_out(component, "width", True)

    @classmethod
    def height_in(cls, component):
        return cls._h_w_out(component, "height", False)

    @classmethod
    def width_in(cls, component):
        return cls._h_w_out(component, "width", False)


# Pre-computed styles:
# https://web-animations.github.io/web-animations-demos/#animate_css/
pulse = Transition(transform=["none", "scale(1.05)", "none"])
bounce = Transition(
    transform=[f"translateY({n}px)" for n in (0, 0, -30, -30, 0, -15, 0, -15, 0)],
    offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1],
)
shake = Transition(
    transform=[f"translate({x}px)" for x in (0, 10, -10, 10, -10, 10, -10, 10, -10, 0)]
)

fade_in = Transition(opacity=[0, 1])
fade_in_slow = Transition(opacity=[0, 0.25, 1], offset=[0, 0.75, 1])
fade_out = Transition(opacity=[1, 0])

fly_in_up = Transition(transform=["translateY(100%) scale(0)", "none"], opacity=[0, 1])
fly_in_down = Transition(
    transform=["translateY(-100%) scale(0)", "none"], opacity=[0, 1]
)
fly_in_left = Transition(
    transform=["translateX(100%) scale(0)", "none"], opacity=[0, 1]
)
fly_in_right = Transition(
    transform=["translateY(-100%) scale(0)", "none"], opacity=[0, 1]
)

fly_out_up = Transition(
    transform=["none", "translateY(-100%) scale(0)"], opacity=[1, 0]
)
fly_out_down = Transition(
    transform=["none", "translateY(100%) scale(0)"], opacity=[1, 0]
)
fly_out_left = Transition(
    transform=["none", "translateX(-100%) scale(0)"], opacity=[1, 0]
)
fly_out_right = Transition(
    transform=["none", "translateX(100%) scale(0)"], opacity=[1, 0]
)

rotate_in = Transition(transform=["none", "rotate(200deg)"])
rotate_out = Transition(transform=["rotate(200deg)", "none"])

zoom_in = Transition(transform=["scale(.3)", "none"])
zoom_out = Transition(transform=["none", "scale(.3)"])

# add a method to the window.Animation class for our convenience
_window.Function(
    """
Animation.prototype.wait = function() {
    return this.finished;
};
"""
)()


class Animation:
    """This is a wrapper around the Browser Animation object.
    It is the return value from animate(), or Effect.animate()
    Can be created in code with a component and an Effect"""

    def __new__(cls, component=None, effect=None, *, _a=None):
        # we just return the animation object
        # the only job of this class is to provide autocompletions
        if _a is not None:
            # we're already an animation
            return _a
        elif component is None or effect is None:
            raise TypeError(
                "An Animation can only be created with a Component (or DOM node) and an Effect"
            )
        el = _dom_node(component)
        keyframes = effect.getKeyframes()
        timings = effect.getTimings()
        return _window.Animation(_a=_window.KeyframeEffect(el, keyframes, timings))

    def __init__(self, component, effect):
        pass

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


def _animate(component, keyframes, options, use_ghost=False):
    el = _dom_node(component)

    if use_ghost:
        _animate_ghost(el, keyframes, options)

    return Animation(_a=el.animate(keyframes, options))


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
    """Create an effect that can later be used to animate a component.
    The first argument should be a Transtion object.
    The remainder of the values are timing options"""

    def __new__(cls, transition=None, **timings):
        return _window.KeyframeEffect(None, transition, timings)

    def __init__(
        self,
        transition=None,
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
        """animate a component using an effect.
        If use_ghost is True a ghost element will be animated.
        use_ghoste allows components to be animated outside of their container
        """
        return Animation(_a=None)  # just so the autocompleter knows the return type

    def getKeyframes(self, component):
        "Returns the computed keyframes that make up this effect"

    def getTiming(self, component):
        "The EffectTiming object associated with the animation"


def animate(
    component,
    transition=None,
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
    component: an anvil Component or Javascript HTMLElement
    transition: Transion object
    **effect_timing: various options to change the behaviour of the animation e.g. duration.

    Anvil specific arguments:
    use_ghost: when set to True will allow the component to be animated outside of its container

    start_at, end_at: Can be set to a component or DOMRect (i.e. a computed position of a component from get_bounding_rect)
    If either start_at or end_at are set this will determine the start/end position of the animationn
    If one value is set and the other omitted the omitted value will be assumed to be the current position of the componenent.
    A ghost element is always used when start_at/end_at are set.
    """
    effect_timing = {
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
    if start_at is not None or end_at is not None:
        # we use a ghost here regardless
        return _animate_from_to(
            component,
            start_at or component,
            end_at or component,
            transition,
            effect_timing,
        )
    return _animate(component, transition, effect_timing, use_ghost)


def is_animating(component) -> bool:
    """Determines whether a component is currently animating"""
    el = _dom_node(component)
    return any(a.playState == "running" for a in el.getAnimations())


def wait_for(animation_or_component):
    """If given an animation equivalent to animateion.wait().
    If given a component, will wait for all running animations on the component to finish"""
    if hasattr(animation_or_component, "finished"):
        _await_promise(animation_or_component.finished)
        return
    el = _dom_node(animation_or_component)
    animations = el.getAnimations()
    _window.Promise.all(list(map(lambda a: a.finished, animations)))


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
    """returns an object with attributes relating to the position of the component on the page: x, y, width, height"""
    if component.__class__ == _window.DOMRect:
        return component
    el = _dom_node(component)
    return DOMRect(obj=el.getBoundingClientRect())


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

    el.style.visibility = "hidden"

    def ghost_finish(e):
        el.style.visibility = "visible"
        ghost.remove()

    ghost.animate(keyframes, options).addEventListener("finish", ghost_finish)


def _animate_from_to(component, c1, c2, t, options):
    el = _dom_node(component)
    pos = el.getBoundingClientRect()
    pos1, pos2 = get_bounding_rect(c1), get_bounding_rect(c2)
    t_fromto = Transition(
        transform=[
            f"translateX({pos1.x - pos.x}px) translateY({pos1.y - pos.y}px)",
            f"translateX({pos2.x - pos.x}px) translateY({pos2.y - pos.y}px)",
        ]
    )
    if pos1.width != pos2.width:
        t_fromto["width"] = [pos1.width, pos2.width]
    if pos1.height != pos2.height:
        t_fromto["height"] = [pos1.height, pos2.height]

    t = (t or {}) | t_fromto

    # we create a ghost node
    return Animation(_a=_animate(component, t, options, use_ghost=True))
