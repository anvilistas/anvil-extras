# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js import await_promise as _await_promise
from anvil.js import get_dom_node as _dom_node
from anvil.js import window as _window

__version__ = "2.2.3"


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


_transforms = {
    "matrix",
    "translate",
    "translateX",
    "translateY",
    "scale",
    "scaleX",
    "scaleY",
    "rotate",
    "skew",
    "skewX",
    "skewY",
    "matrix3d",
    "translate3d",
    "translateZ",
    "scale3d",
    "scaleZ",
    "rotate3d",
    "rotateX",
    "rotateY",
    "rotateZ",
    "perspective",
}


class Transition(dict):
    """Create a transtion object.
    Takes CSS/transform property names as keyword arguments and each value should be a list of frames for that property.
    The number of frames must match across all properties.

    e.g. slide_right = Transition(translateX=[0, "100%"])

    Each list item represents a CSS value to be applied across the transition.
    Typically the first value is the start of the transition and the last value is the end.
    Lists can be more than 2 values in which case the transition will be split across the values evenly.
    You can customize the even split by setting an offset that has values from 0, 1

    e.g. fade_in_slow = Transition(opacity=[0, 0.25, 1], offset=[0, 0.75, 1])

    Transition objects can be combined with the | operator (which behaves like merging dictionaries)
    e.g. t = reversed(slide_right) | zoom_in | fade_in | Transition.height_in(component)
    """

    def __new__(cls, **transitions):
        t_keys = set()
        t_len = None
        for key, val in transitions.items():
            assert (
                type(val) is list or type(val) is tuple
            ), "all tranistion must be lists"
            if key not in _transforms:
                continue
            t_keys.add(key)
            if t_len is None:
                t_len = len(val)
            else:
                assert t_len == len(
                    val
                ), "transform based transitions must all have the same frame length"
        return cls._create(transitions, frozenset(t_keys), t_len)

    def __init__(
        self,
        *,
        opacity=None,
        scale=None,
        translateX=None,
        translateY=None,
        rotate=None,
        backgroundColor=None,
        offset=None,
        **css_transitions,
    ):
        # just for the autocomplete - some common CSS transitions
        pass

    @classmethod
    def _create(cls, transitions, transform_keys, transform_len):
        self = dict.__new__(cls)
        dict.__init__(self, **transitions)
        self._t_keys = transform_keys
        self._t_len = transform_len
        return self

    def __repr__(self):
        return f"Transition({dict.__repr__(self)})"

    @staticmethod
    def _check_other(other):
        if isinstance(other, Transition):
            return other
        elif isinstance(other, dict):
            return Transition(**other)
        else:
            return NotImplemented

    def __or__(self, other):
        other = self._check_other(other)
        if other is NotImplemented:
            return NotImplemented

        self_len, other_len = self._t_len, other._t_len

        merged = dict.__or__(self, other)

        if self_len is None:
            return self._create(merged, other._t_keys, other_len)
        elif other_len is None:
            return self._create(merged, self._t_keys, self_len)
        elif other_len != self_len:
            raise ValueError(
                "can't combine Transition objects with different frame lengths for transform based transitions"
            )

        return self._create(merged, self._t_keys | other._t_keys, self_len)

    def __ror__(self, other):
        other = self._check_other(other)
        if other is NotImplemented:
            return NotImplemented
        return other.__or__(self)

    def __reversed__(self):
        reverse = {}
        for key, val in self.items():
            reverse[key] = list(reversed(val))
        return self._create(reverse, self._t_keys, self._t_len)

    @classmethod
    def _h_w(cls, component, attr, out=True):
        hw = get_bounding_rect(component)[attr]
        return cls(**{attr: [f"{hw}px", 0] if out else [0, f"{hw}px"]})

    @classmethod
    def height_out(cls, component):
        return cls._h_w(component, "height", True)

    @classmethod
    def width_out(cls, component):
        return cls._h_w(component, "width", True)

    @classmethod
    def height_in(cls, component):
        return cls._h_w(component, "height", False)

    @classmethod
    def width_in(cls, component):
        return cls._h_w(component, "width", False)

    def _compute(self):
        # combines transforms into a single string
        copy = self.copy()
        if self._t_len is None:
            return copy
        transform = [""] * self._t_len

        for key in self._t_keys:
            frames = copy.pop(key, None)
            if frames is None:
                # This shouldn't happen
                continue
            for i, val in enumerate(frames):
                transform[i] += f"{key}({val}) "
        copy["transform"] = transform

        return copy


# Pre-computed styles:
# https://web-animations.github.io/web-animations-demos/#animate_CSS/
pulse = Transition(scale=[1, 1.05, 1])
bounce = Transition(
    translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0],
    offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1],
)
shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])

fade_in = Transition(opacity=[0, 1])
fade_in_slow = Transition(opacity=[0, 0.25, 1], offset=[0, 0.75, 1])
fade_out = reversed(fade_in)

slide_in_up = Transition(translateY=["100%", 0])
slide_in_down = Transition(translateY=["-100%", 0])
slide_in_left = Transition(translateX=["-100%", 0])
slide_in_right = Transition(translateX=["100%", 0])

slide_out_up = reversed(slide_in_down)
slide_out_down = reversed(slide_in_up)
slide_out_left = reversed(slide_in_left)
slide_out_right = reversed(slide_in_right)

rotate = Transition(rotate=[0, "360deg"])

zoom_in = Transition(scale=[0.3, 1])
zoom_out = reversed(zoom_in)

fly_in_up = slide_in_up | zoom_in | fade_in
fly_in_down = slide_in_down | zoom_in | fade_in
fly_in_left = slide_in_left | zoom_in | fade_in
fly_in_right = slide_in_right | zoom_in | fade_in

fly_out_up = reversed(fly_in_down)
fly_out_down = reversed(fly_in_up)
fly_out_left = reversed(fly_in_left)
fly_out_right = reversed(fly_in_right)


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
        "set a callback for when the animation is cancelled"

    @property
    def onremove(self):
        "set a callback for when the animation is removed"


def _animate(component, keyframes, options, use_ghost=False):
    if isinstance(keyframes, Transition):
        keyframes = keyframes._compute()
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
    The first argument should be a Transition object.
    The remainder of the values are timing options"""

    def __new__(cls, transition=None, duration=333, **timings):
        if isinstance(transition, Transition):
            transition = transition._compute()
        timings["duration"] = duration
        return _window.KeyframeEffect(None, transition, timings)

    def __init__(
        self,
        transition=None,
        duration=333,
        *,
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
    duration=333,
    *,
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
    transition: Transition object
    **effect_timing: various options to change the behaviour of the animation e.g. duration.

    Anvil specific arguments:
    use_ghost: when set to True will allow the component to be animated outside of its container

    start_at, end_at: Can be set to a component or DOMRect (i.e. a computed position of a component from get_bounding_rect)
    If either start_at or end_at are set this will determine the start/end position of the animation
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


def is_animating(component, include_children=False) -> bool:
    """Determines whether a component is currently animating"""
    el = _dom_node(component)
    return any(
        a.playState == "running"
        for a in el.getAnimations({"subtree": include_children})
    )


def wait_for(animation_or_component, include_children=False):
    """If given an animation equivalent to animateion.wait().
    If given a component, will wait for all running animations on the component to finish
    """
    if hasattr(animation_or_component, "finished"):
        _await_promise(animation_or_component.finished)
        return
    el = _dom_node(animation_or_component)
    animations = el.getAnimations({"subtree": include_children})
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
    # TODO if web animations support GroupAnimations in the future we should use that here
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
        translateX=[f"{pos1.x - pos.x}px", f"{pos2.x - pos.x}px"],
        translateY=[f"{pos1.y - pos.y}px", f"{pos2.y - pos.y}px"],
    )
    if pos1.width != pos2.width:
        t_fromto["width"] = [pos1.width, pos2.width]
    if pos1.height != pos2.height:
        t_fromto["height"] = [pos1.height, pos2.height]

    t = (t or {}) | t_fromto

    # we create a ghost node
    return Animation(_a=_animate(component, t, options, use_ghost=True))
