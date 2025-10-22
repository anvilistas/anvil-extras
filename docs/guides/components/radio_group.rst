RadioGroup
===========

A flexible container that groups multiple ``anvil.RadioButton`` components so that only one
can be selected at a time. You can either:

- add individual ``RadioButton`` components as children of the group, or
- set the ``items`` property (similar to an Anvil ``Dropdown``) to auto-generate buttons.

The currently selected value is exposed via ``selected_value`` and a ``change`` event
is fired whenever the selection changes.


Usage
-----

Add as a container and append buttons
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from anvil import RadioButton
    from anvil_extras.RadioGroup import RadioGroup


    class Form(FormTemplate):
        def __init__(self, **properties):
            # You can do this in code or via the Designer:
            # - Designer: Drag a RadioGroup onto your form, then drop RadioButtons into it.
            # - Code: Create a RadioGroup and add RadioButtons as children.
            self.radio_group = RadioGroup()
            self.add_component(self.radio_group)
            self.radio_group.add_component(RadioButton(text="Option A", value="a"))
            self.radio_group.add_component(RadioButton(text="Option B", value="b"))
            self.radio_group.add_event_handler("change", self.radio_group_change)

    def radio_group_change(self, **event_args):
        # Read the logical value of the selected option
        print(self.radio_group.selected_value)  # -> "a" or "b"



Use the items property (like Dropdown)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``items`` may be a list of strings or a list of ``(text, value)`` tuples:

.. code-block:: python

    from anvil_extras.RadioGroup import RadioGroup

    # Simple list of strings: value equals the text
    self.radio_group = RadioGroup(items=["One", "Two", "Three"])  # selected_value is one of the strings

    # List of (text, value) pairs: logical value is separate from the label
    self.radio_group.items = [("Apples", "apples"), ("Oranges", "oranges"), ("Pears", "pears")]

    # Reading the selection returns the logical value (e.g. "oranges"):
    print(self.radio_group.selected_value)

    # Programmatic selection: set the logical value directly
    self.radio_group.selected_value = "oranges"  # selects "Oranges"


Group existing RadioButtons on your form
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have individual ``RadioButton`` components on a form, you can group them:

.. code-block:: python

    from anvil_extras.RadioGroup import RadioGroup

    # If you already have RadioButtons on your form (e.g. placed in the Designer),
    # you can add group behaviour without moving them into the RadioGroup container.
    # This is especially useful when buttons may not be on-screen yet and
    # radio_buttons.group_value would otherwise be None.
    # The group ensures mutual exclusivity and consistent change events.
    self.radio_group = RadioGroup()
    self.radio_group.buttons = [self.radio_button_1, self.radio_button_2]
    self.radio_group.add_event_handler("change", self.radio_group_change)

    # Alternatively, pass the buttons in the constructor
    self.radio_group = RadioGroup(buttons=[self.radio_button_1, self.radio_button_2])
    self.radio_group.add_event_handler("change", self.radio_group_change)


Properties
----------

:selected_value: object | None

    The logical value of the selected option. When using ``items`` with ``(text, value)``
    pairs, this returns the ``value`` part. When using a list of strings, this is the string.
    Set to a matching value to programmatically select an option, or to ``None`` to clear.

:gap: string | float | int

    Spacing between radio buttons. Accepts a number (pixels) or a CSS length string
    (e.g. ``"12px"``, ``"0.5rem"``).

:spacing: spacing

    Standard Anvil container spacing

:direction: enum

    Layout direction of the group: ``"horizontal"`` (default) or ``"vertical"``.

:align: enum

    Alignment of buttons within the group. One of
    ``"left"``, ``"center"``, ``"right"``, ``"space-evenly"``, ``"space-between"``,
    ``"space-around"``. In horizontal layout this controls horizontal distribution;
    in vertical layout it controls cross-axis alignment.

:visible: bool

    Whether the component is visible.

:items: list[str] | list[tuple[str, Any]]

    Use to auto-generate buttons. Strings produce labels with the same value; tuples
    of ``(text, value)`` let you separate display text and logical value.

:buttons: list[anvil.RadioButton]

    Assign an explicit list of existing ``RadioButton`` components to be managed by
    the group. When set, event handlers are attached and the buttons are grouped so
    only one can be selected at a time. You can also provide this in the constructor,
    e.g. ``RadioGroup(buttons=[rb1, rb2])``.


Events
------

:change:

    Fired when the selection changes. This is the default event. Use
    ``self.radio_group.selected_value`` inside the handler to read the current value.

:show:

    Fired when the component is shown.

:hide:

    Fired when the component is hidden.


Notes
-----

- When ``items`` contains ``(text, value)`` pairs, ``selected_value`` returns the
  ``value``; with a simple list of strings, it returns the string itself.
- Setting ``selected_value`` to a value that doesn't exist will clear the selection.
- For tuple ``items``, set ``selected_value`` to the tuple's logical value (e.g. ``"oranges"``)
  at any time to select that option.
- ``align="left"``/``"right"`` map to flexbox ``flex-start``/``flex-end`` under the hood.
