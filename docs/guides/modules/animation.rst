Animation
=========
A wrapper around the `Web Animations API <https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API>`_

Interfaces
----------
.. class:: Animation(component, effect)

    An Animation object will be returned from the ``Effect.animate()`` method and the :attr:`animate()` function.
    Provides playback control for an animation.

.. class:: Effect(transiton, **effect_timing_options)

    A combination of a :class:`Transition` object and timing options.
    An effect can be used to animate an Anvil Component with its ``.animate()`` method.
    ``effect_timing_options`` are equivalent to those listed at `EffectTiming <https://developer.mozilla.org/en-US/docs/Web/API/EffectTiming>`_

.. class:: Transition(**css_frames)

    A dictionary-based class. Each key should be a CSS property in camelCase with a list of frames.
    Each frame in the list represents a style to hit during the animation.
    The first value in the list is where the animation starts and the final value is where the animation ends.
    See :any:`Pre-computed Transitions<transition-examples>` for examples.


.. function:: animate(component, transition, **timing_options)

    A shortcut for animating an Anvil Component. Returns an Animation instance.



Examples
--------

Animate on show
***************

Use the show event to animate an Anvil Component.
This could could also be at the end of an ``__init__`` function after any expensive operations.

Creating an :class:`Effect` allows the effect to be re-used by multiple components.

.. code-block:: python

    from anvil_extras.animation import Effect, Transition

    fade_in = Transition(opacity=[0, 1])
    effect = Effect(fade_in, duration=500)

    def card_show(self, **event_args):
        effect.animate(self.card)


Alternatively use :attr:`animate` with a :class:`Transition` and timing options.

.. code-block:: python

    from anvil_extras.animation import animate, fade_in

    def card_show(self, **event_args):
        animate(self.card, fade_in, duration=500)


Animate on remove
*****************

When a component is removed we need to wait for an animation to complete before removing it.

.. code-block:: python

    from anvil_extras.animation import animate, fade_out, Easing, Effect

    leave_effect = Effect(fade_out, duration=500, easing=Easing.ease_out)


    def button_click(self, **event_args):
        if self.card.parent is not None:
            # we can't do this in the hide event because we're already off the screen!
            leave_effect.animate(self.card).wait()
            self.card.remove_from_parent()


Combine Transitions
*******************

Transitions can be combined with the `|` operator. They will be merged like dictionaries.

.. code-block:: python

    from anvil_extras.animation import animate, zoom_out, fade_out, Transition

    zoom_fade_out = zoom_out | fade_out
    zoom_fade_in = reversed(zoom_fade_out)

    def button_click(self, **event_args):
        if self.card.parent is not None:
            t = zoom_fade_out | Transition.height_out(component)
            animate(self.card, t, duration=500).wait()
            self.card.remove_from_parent()


Animate on visible change
*************************

Some work is needed to animate a Component when the visibility property changes.
A helper function might look something like.

.. code-block:: python

    from anvil_extras.animation import Transition, wait_for

    zoom = Transition(scale=[.3, 1], opacity=[0, 1])

    def visible_change(self, component):
        if is_animating(component):
            return

        is_visible = component.visible
        if not is_visible:
            # set this now because we need it on the screen to measure its height
            # if you have a show event for this component - it may also fire
            component.visible = True
            direction = "normal"
        else:
            direction = "reverse"

        t = zoom | Transition.height_in(component)
        animate(component, t, duration=900, direction=direction)

        if is_visible:
            # we're animating - wait for the animation to finish before setting visible to False
            wait_for(component) # equivalent to animation.wait() or wait_for(animation)
            component.visible = False



Swap Elements
*************

Swapping elements requires us to animate from one component to another.
We wait for the animation to finish.
Then, remove the components and add them back in their new positions.
Removing and adding components happens quickly so that the user only sees the components switching places.

.. code-block:: python

    from anvil_extras.animation import animate

    def button_click(self, **event_args):
        # animate wait then remove and re-add
        components = self.linear_panel.get_components()
        c0, c1 = components[0], components[1]
        animate(c0, end_at=c1)
        animate(c1, end_at=c0).wait()
        c0.remove_from_parent()
        c1.remove_from_parent()
        self.linear_panel.add_component(c0, index=0)
        self.linear_panel.add_component(c1, index=0)



An alternative version would get the positions of the components.
Then remove and add the components to their new positions.
Finally animating the components starting from whence they came to their new positions.


.. code-block:: python

    from anvil_extras.animation import animate, get_bounding_rect, is_animating

    def button_click(self, **event_args):
        # get positions, remove, change positions, reverse animate
        components = self.linear_panel.get_components()
        c0, c1 = components[0], components[1]
        if is_animating(c0) or is_animating(c1):
            return
        p0, p1 = get_bounding_rect(c0), get_bounding_rect(c1)
        c0.remove_from_parent()
        c1.remove_from_parent()
        self.linear_panel.add_component(c0, index=0)
        self.linear_panel.add_component(c1, index=0)
        animate(c0, start_at=p0)
        animate(c1, start_at=p1)



Switch positions might be useful in a RepatingPanel.
Here's what that code might look like.


.. code-block:: python

    from anvil_extras.animation import animate

    class Form1(Form1Template):
        def __init__(self, **properties):
            ...
            self.repeating_panel_1.set_event_handler('x-swap', self.swap)


        def swap(self, component, is_up, **event_args):
            """this event is raised by a child component"""
            items = self.repeating_panel_1.items
            components = self.repeating_panel_1.get_components()
            i = components.index(component)
            j = i - 1 if is_up else i + 1
            if j < 0:
                # we can't go negative
                return
            c1 = component
            try:
                c2 = components[j]
            except IndexError:
                return

            animate(c1, end_at=c2)
            animate(c2, end_at=c1).wait()
            items[i], items[j] = items[j], items[i]
            self.repeating_panel_1.items = items



    class ItemTemplate1(ItemTemplate1Template):
        def __init__(self, **properties):
            # Set Form properties and Data Bindings.
            self.init_components(**properties)
            # Any code you write here will run when the form opens.

        def up_btn_click(self, **event_args):
            """This method is called when the button is clicked"""
            self.parent.raise_event('x-swap', component=self, is_up=True)

        def down_btn_click(self, **event_args):
            """This method is called when the button is clicked"""
            self.parent.raise_event('x-swap', component=self, is_up=False)


Full API
--------

.. function:: is_animating(component)

    Returns a boolean as to whether the component is animating.

.. function:: wait_for(component_or_animation)

    If given an animation equivalent to ``animation.wait()``.
    If given a component, will wait for all running animations on the component to finish.


.. function:: animate(component, transition=None, start_at=None, end_at=None, use_ghost=False, **effect_timing_options)
    :noindex:

    ``component``: an anvil Component or Javascript HTMLElement

    ``transition``: Transition object

    ``effect_timing_options``: `various options <https://developer.mozilla.org/en-US/docs/Web/API/EffectTiming>`_ to change the behaviour of the animation e.g. ``duration=500``.

    ``use_ghost``: when set to ``True``, will animate a ghost element (i.e. a visual copy).
    Using a ghost element will allow the component to be animated outside of its container

    ``start_at``, ``end_at``: Can be set to a ``Component`` or ``DOMRect`` (i.e. a computed position of a component from ``get_bounding_rect``)
    If either ``start_at`` or ``end_at`` are set this will determine the start/end position of the animation
    If one value is set and the other omitted the omitted value will be assumed to be the current position of the component.
    A ghost element is always used when ``start_at`` / ``end_at`` are set.

.. function:: get_bounding_rect(component)

    Returns a ``DOMRect`` object. A convenient way to get the ``height``, ``width``, ``x``, ``y`` values of a *component*.
    Where the ``x``, ``y`` are the absolute positions on the page from the top left corner.


.. class:: Transition(cssProp0=list[str], cssProp1=list[str], transformProp0=list[str], offset=list[int | float])
    :noindex:

    Takes CSS/transform property names as keyword arguments and each value should be a list of frames for that property.
    The number of frames must match across all properties.

    ``slide_right = Transition(translateX=[0, "100%"])``

    Each list item represents a CSS value to be applied across the transition.
    Typically the first value is the start of the transition and the last value is the end.
    Lists can be more than 2 values, in which case the transition will be split across the values evenly.
    You can customize the even split by setting an offset that has values from 0, 1

    ``fade_in_slow = Transition(opacity=[0, 0.25, 1], offset=[0, 0.75, 1])``

    Transition objects can be combined with the ``|`` operator (which behaves like merging dictionaries)
    ``t = reversed(slide_right) | zoom_in | fade_in | Transtion.height_in(component)``

    .. classmethod:: height_out(cls, component)

        Returns a Transition starting from the current height of the component and ending at 0 height.

    .. classmethod:: height_in(cls, component)

        Returns a Transition starting from height 0 and ending at the current height of the component.

    .. classmethod:: width_out(cls, component)

        Returns a Transition starting from the current width of the component and ending at 0 width.

    .. classmethod:: width_in(cls, component)

        Returns a Transition starting from width 0 and ending at the current width of the component.

    .. describe:: reversed(transition)

        Returns a Transition with all frames reversed for each property.

.. class:: Effect(transition, **effect_timing_options):
    :noindex:

    Create an effect that can later be used to animate a component.
    The first argument should be a Transition object.
    Other keyword arguments should be `effect timing options <https://developer.mozilla.org/en-US/docs/Web/API/EffectTiming>`_.

    .. method:: animate(self, component, use_ghost=False)
        :noindex:

        animate a component using an effect object.
        If ``use_ghost`` is ``True`` a ghost element will be animated.
        Returns an Animation instance.

    .. method:: getKeyframes(self, component)

        Returns the computed keyframes that make up this effect. Can be used in place of the ``transition`` argument in other functions.

    .. method:: getTiming(self, component)

        Returns the EffectTiming object associated with this effect.


.. class:: Animation(component, effect):
    :noindex:

    An Animation object will be returned from the ``Effect.animate()`` method and the ``animate()`` function.
    Provides playback control for an animation.

    .. method:: cancel(self)

        abort animation playback

    .. method:: commitStyles(self)

        Commits the end styling state of an animation to the element

    .. method:: finish(self)

        Seeks the end of an animation

    .. method:: pause(self)

        Suspends playing of an animation

    .. method:: play(self)

        Starts or resumes playing of an animation, or begins the animation again if it previously finished.

    .. method:: persist(self)

        Explicitly persists an animation, when it would otherwise be removed.

    .. method:: reverse(self)

        Reverses playback direction and plays

    .. method:: updatePlaybackRate(self, playback_rate)

        The new speed to set. A positive number (to speed up or slow down the animation), a negative number (to reverse), or zero (to pause).

    .. method:: wait(self)

        Animations are not blocking. Call the wait function to wait for an animation to finish in a blocking way

    .. attribute:: playbackRate

        gets or sets the playback rate

    .. attribute:: onfinish

        set a callback for when the animation finishes

    .. attribute:: oncancel

        set a callback for when the animation is cancelled

    .. attribute:: onremove

        set a callback for when the animation is removed


.. attribute:: Easing

    An Enum like instance with some common easing values.

    ``Easing.ease``, ``Easing.ease_in``, ``Easing.ease_out``, ``Easing.ease_in_out`` and ``Easing.linear``.

    .. method:: cubic_bezier(po, p1, p2, p3)

        Create a ``cubic_bezier`` easing value from 4 numerical values.


.. _transition-examples:

Pre-computed Transitions
------------------------

Attention Seekers
*****************
* ``pulse = Transition(scale=[1, 1.05, 1])``
* ``bounce = Transition(translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])``
* ``shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])``

Fades
*****

* ``fade_in = Transition(opacity=[0, 1])``
* ``fade_in_slow = Transition(opacity=[0, 0.25, 1], offset=[0, 0.75, 1])``
* ``fade_out = reversed(fade_in)``

Slides
******

* ``slide_in_up = Transition(translateY=["100%", 0])``
* ``slide_in_down = Transition(translateY=["-100%", 0])``
* ``slide_in_left = Transition(translateX=["-100%", 0])``
* ``slide_in_right = Transition(translateX=["100%", 0])``

* ``slide_out_up = reversed(slide_in_up)``
* ``slide_out_down = reversed(slide_in_down)``
* ``slide_out_left = reversed(slide_in_left)``
* ``slide_out_right = reversed(slide_in_right)``


Rotate
******


* ``rotate_in = Transition(rotate=[0, "200deg"])``
* ``rotate_out = reversed(rotate_in)``


Zoom
****

* ``zoom_in = Transition(scale=[.3, 1])``
* ``zoom_out = reversed(zoom_in)``


Fly
***

* ``fly_in_up = slide_in_up | zoom_in | fade_in``
* ``fly_in_down = slide_in_down | zoom_in | fade_in``
* ``fly_in_left = slide_in_left | zoom_in | fade_in``
* ``fly_in_right = slide_in_right | zoom_in | fade_in``

* ``fly_out_up = reversed(fly_in_up)``
* ``fly_out_down = reversed(fly_in_down)``
* ``fly_out_left = reversed(fly_in_left)``
* ``fly_out_right = reversed(fly_in_right)``
