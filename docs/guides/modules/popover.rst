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
Popovers are already included with anvil since anvil `ships with bootstrap <https://anvil.works/docs/client/javascript#already-included-javascript>`_.

This module provides a python wrapper around `bootstrap popovers <https://getbootstrap.com/docs/3.4/javascript/#popovers>`_.
When the ``popover`` module is imported Links and Buttons get two additional methods - ``pop`` and ``popover``.


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

.. method:: popover(self, content, title='', placement='right', trigger='click', animation=True, delay={"show": 100, "hide": 100}, max_width=None, auto_dismiss=True)

    popover is a method that can be used with any ``Button`` or ``Link``.

    .. describe:: self

        the ``Button`` or ``Link`` used. No need to worry about this argument when using popover as a method e.g. ``self.button_1.popover(content='example text')``

    .. describe:: content

        content can be a string or an anvil component. If an anvil component is used - that component will have a new attribute ``popper`` added.
        This allows the the content form to close itself using ``self.popper.pop('hide')``.

    .. describe:: title

        optional string.

    .. describe:: placement

        One of ``'right'``, ``'left'``, ``'top'``, ``'bottom'``. If using ``left`` or ``right`` it may be best to place the component in a ``FlowPanel``.

    .. describe:: trigger

        One of ``'manual'``, ``'focus'``, ``'hover'``, ``'click'``, (can be a combination of two e.g. ``'hover focus'``). ``'stickyhover'`` is also available.

    .. describe:: animation

        ``True`` or ``False``

    .. describe:: delay

        A dictionary with the keys ``'show'`` and ``'hide'``. The values for ``'show'`` and ``'hide'`` are in milliseconds.

    .. describe:: max_width

        bootstrap default is 276px you might want this wider

    .. describe:: auto_dismiss

        when clicking outside a popover the popover will be closed. Setting this flag to ``False`` overrides that behaviour.


.. method:: pop(self, behaviour)

    pop is a method that can be used with any ``Button`` or ``Link`` that has a ``popover``

    .. describe:: self

        the ``Button`` or ``Link`` used. No need to worry about this argument when using ``self.button_1.pop('show')``

    .. describe:: behaviour

        ``'show'``, ``'hide'``, ``'toggle'``, ``'destroy'``. Also includes ``'shown'`` and ``'is_visible'`` which return a ``boolean``.



.. function:: dismiss_on_outside_click(dismiss=True)

    by default if you click outside of a popover the popover will close. This behaviour can be overridden globally by calling this function. It can also be set per popover using the ``auto_dismiss`` argument.

.. function:: set_default_max_width(width)

    update the default max width - this is 276px by default - useful for wider components.
