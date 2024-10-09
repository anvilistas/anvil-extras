Popovers
========
A client module that allows bootstrap popovers in anvil

Live Example: `popover-example.anvil.app <https://popover-example.anvil.app>`_

Example Clone Link:

.. image:: https://anvil.works/img/forum/copy-app.png
   :height: 40px
   :target: https://anvil.works/build#clone:YRRNNZJZV5IJM6NX=ACDZQ3LRIADCMMGFANOJZG5N



Introduction
------------
Add small overlays of content to anvil components.

When the ``popover`` module is imported, all anvil components get two additional methods - ``pop`` and ``popover``.


Usage
-----

.. code-block:: python

    from anvil_extras import popover
    # importing the module adds the popover method to Button and Link

        self.button = Button()
        self.button.popover(content='example text', title='Popover', placement="top")


.. code-block:: python

    from anvil_extras import popover

        self.button_1.popover(Form2(), trigger="manual")
        # content can be an anvil component

        def button_1_click(self, **event_args):
            if self.button_1.pop("is_visible"):
                self.button_1.pop("hide")
            else:
                self.button_1.pop("show")
            # equivalent to self.button_1.pop("toggle")

API
---

.. method:: popover(self, content, title='', placement='right', trigger='click', animation=True, delay={"show": 100, "hide": 100}, max_width=None, auto_dismiss=True, container="body")

    popover is a method that can be used with any anvil component. Commonly used on ``Button`` and ``Link`` components.

    .. describe:: self

        the component used. No need to worry about this argument when using popover as a method e.g. ``self.button_1.popover(content='example text')``

    .. describe:: content

        content can be a string or an anvil component. If an anvil component is used - that component will have a new attribute ``popper`` added.
        This allows the content form to close itself using ``self.popper.pop('hide')``.

    .. describe:: title

        optional string.

    .. describe:: placement

        One of ``'right'``, ``'left'``, ``'top'`` or ``'bottom'``.
        If using ``left`` or ``right`` it may be best to place the component in a ``FlowPanel``.
        If there is limited space in the preferred placement, then the popover will be placed in the opposite direction.

    .. describe:: trigger

        One of ``'manual'``, ``'focus'``, ``'hover'``, ``'click'``, (can be a combination of two e.g. ``'hover focus'``). ``'stickyhover'`` is also available.

    .. describe:: animation

        ``True`` or ``False``

    .. describe:: delay

        An int, float, or a dictionary with the keys ``'show'`` and ``'hide'``. The values for ``'show'`` and ``'hide'`` are in milliseconds.

    .. describe:: max_width

        Default is 276px you might want this wider

    .. describe:: auto_dismiss

        When clicking outside a popover the popover will be closed. Setting this flag to ``False`` overrides that behaviour.
        Note this is ignored if ``dismiss_on_outside_click()`` is used to set the global behaviour to ``False``

    .. describe:: container

        Set the container of the popover to an element or selector on the page. The default value is ``"body"``.



.. method:: pop(self, behaviour)

    pop is a method that can be used with any component that has a ``popover``

    .. describe:: self

        the component used. No need to worry about this argument when using ``self.button_1.pop('show')``

    .. describe:: behaviour

        ``'show'``, ``'hide'``, ``'toggle'``, ``'destroy'``. Also includes ``'shown'`` and ``'is_visible'``, which return a ``boolean``.



.. function:: dismiss_on_outside_click(dismiss=True)

    By default, if you click outside of a popover the popover will close. This behaviour can be overridden globally by calling this function. It can also be set per popover using the ``auto_dismiss`` argument.
    Note that popovers will always be dismissed when the page is scrolled. This prevents popovers from appearing in weird places on the page.


.. function:: set_default_container(selector_or_element)

    The default container is ``"body"``. This is used since it prevents overflow issues with popovers nested in the anvil component hierarchy.
    If you want your popovers to be inserted into a different element, either change this setting globally or use the ``container`` argument per popover.


.. function:: set_default_max_width(width)

    update the default max width - this is 276px by default - useful for wider components.

.. function:: has_popover(component)

    Returns a ``bool`` as to whether the component has a popover. A useful flag to prevent creating unnecessary popovers.



Popover on disabled components
------------------------------

It is not possible to use a popover on a disabled component.
This is because there are no pointer events on disabled components and so events like hover won't fire.
If you need a popover on a disabled component wrap the component in something like a ``FlowPanel`` or ``LinearPanel``
and add the popover to the container instead.


Styling
-------

The following variables can be overridden in your theme.css to style the popovers.

.. code-block:: css

    :root {
        --ae-popover-bg: #fff;
        --ae-popover-border: rgba(0, 0, 0, 0.2);
        --ae-popover-shadow: 0 5px 10px var(--ae-popover-border, rgba(0, 0, 0, 0.2));
        --ae-popover-title-bg: #f7f7f7;
        --ae-popover-title-border: #ebebeb;
    }
