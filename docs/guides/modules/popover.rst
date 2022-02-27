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
Popovers are already included with Anvil since Anvil `ships with bootstrap <https://anvil.works/docs/client/javascript#already-included-javascript>`_.

This module provides a python wrapper around `bootstrap popovers <https://getbootstrap.com/docs/3.4/javascript/#popovers>`_.
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

.. method:: popover(self, content, title='', placement='right', trigger='click', animation=True, delay={"show": 100, "hide": 100}, max_width=None, auto_dismiss=True, dismiss_on_scroll=True, container="body")

    popover is a method that can be used with any anvil component. Commonly used on ``Button`` and ``Link`` components.

    .. describe:: self

        the component used. No need to worry about this argument when using popover as a method e.g. ``self.button_1.popover(content='example text')``

    .. describe:: content

        content can be a string or an anvil component. If an anvil component is used - that component will have a new attribute ``popper`` added.
        This allows the content form to close itself using ``self.popper.pop('hide')``.

    .. describe:: title

        optional string.

    .. describe:: placement

        One of ``'right'``, ``'left'``, ``'top'``, ``'bottom'`` or ``'auto'``.
        If using ``left`` or ``right`` it may be best to place the component in a ``FlowPanel``.
        ``'auto'`` can be combined with other values e.g. ``'auto bottom'``.

    .. describe:: trigger

        One of ``'manual'``, ``'focus'``, ``'hover'``, ``'click'``, (can be a combination of two e.g. ``'hover focus'``). ``'stickyhover'`` is also available.

    .. describe:: animation

        ``True`` or ``False``

    .. describe:: delay

        A dictionary with the keys ``'show'`` and ``'hide'``. The values for ``'show'`` and ``'hide'`` are in milliseconds.

    .. describe:: max_width

        bootstrap default is 276px you might want this wider

    .. describe:: auto_dismiss

        When clicking outside a popover the popover will be closed. Setting this flag to ``False`` overrides that behaviour.
        Note that popovers will always be dismissed when the page is scrolled. This prevents popovers from appearing in weird places on the page.
        Note this is ignored if ``dismiss_on_outside_click()`` is used to set the global behaviour to ``False``

    .. describe:: dismiss_on_scroll

        All popovers are hidden when the page is scrolled. See the ``dismiss_on_scroll`` function for more details.
        Setting this to ``False`` may not be what you want unless you've adjusted the container of the popover.
        This argument will be ignored if set globally to ``False`` using ``dismiss_on_scroll(dismiss=False)``.

    .. describe:: container

        Set the container of the popover to an element or selector on the page. The default value is ``"body"``.



.. method:: pop(self, behaviour)

    pop is a method that can be used with any component that has a ``popover``

    .. describe:: self

        the component used. No need to worry about this argument when using ``self.button_1.pop('show')``

    .. describe:: behaviour

        ``'show'``, ``'hide'``, ``'toggle'``, ``'destroy'``. Also includes ``'shown'`` and ``'is_visible'``, which return a ``boolean``.
        ``'update'`` will update the popover's position. This is useful when a popover's height changes dynamically.



.. function:: dismiss_on_outside_click(dismiss=True)

    By default, if you click outside of a popover the popover will close. This behaviour can be overridden globally by calling this function. It can also be set per popover using the ``auto_dismiss`` argument.
    Note that popovers will always be dismissed when the page is scrolled. This prevents popovers from appearing in weird places on the page.

.. function:: dismiss_on_scroll(dismiss=True)

    By default, if you scroll the popover will close. This behaviour can be overridden globally by calling this function. It can also be set per popover using the ``dismiss_on_scroll`` argument.
    Note that popovers will not scroll with their parents by default since they are fixed on the body of the page.
    If you use this method it should be combined with either, setting the default container to something other than ``"body"``.


.. function:: set_default_container(selector_or_element)

    The default container is ``"body"``. This is used since it prevents overflow issues with popovers nested in the anvil component hierarchy.
    However, it does prevent popovers from scrolling with their attached elements.
    If you want your popovers to scroll with their popper element, either change this setting globally or use the ``container`` argument per popover.


.. function:: set_default_max_width(width)

    update the default max width - this is 276px by default - useful for wider components.

.. function:: has_popover(component)

    Returns a ``bool`` as to whether the component has a popover. A useful flag to prevent creating unnecessary popovers.



Scrolling in Material Design
----------------------------

To support scrolling in Material Design the container element should be a div element within the standard-page.html.
It should be nested within the ``.content`` div.

You can adjust the HTML as follows.

.. code-block:: html

    <div class="content">
        <div anvil-slot-repeat="default" class="anvil-measure-this"></div>
        <div class="placeholder drop-here" anvil-if-slot-empty="default" anvil-drop-slot="default">Drop a ColumnPanel here.</div>
        <div id="popover-container" style="position:relative;"></div>
    </div>


.. code-block:: python

    from anvil_extras import popover

    popover.set_default_container("#popover-container")
    popover.dismiss_on_scroll(False)



Alternatively you could dynamically insert the container component in your MainForm with python.
(Assuming your main form uses the standard-page.html)

.. code-block:: python

    import anvil.js
    from anvil.js.window import document
    from anvil_extras import popover


    popover_container = document.createElement("div")
    popover_container.style.position = "relative"
    popover.set_default_container(popover_container)
    popover.dismiss_on_scroll(False)


    class MainForm(MainFormTemplate):
        def __init__(self, **event_args):
            content_div = anvil.js.get_dom_node(self).querySelector(".content")
            content_div.appendChild(popover_container)
