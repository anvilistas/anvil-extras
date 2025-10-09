CheckBoxGroup
=============

A flexible container that groups multiple ``anvil.CheckBox`` components for multi-select
functionality. You can either:

- add individual ``CheckBox`` components as children of the group, or
- set the ``items`` property (similar to an Anvil ``Dropdown``) to auto-generate checkboxes.

The currently selected values are exposed via ``selected_values`` (a list) and a ``change`` event
is fired whenever any checkbox selection changes.


Usage
-----

Add as a container and append checkboxes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from anvil import CheckBox
    from anvil_extras import CheckBoxGroup


    class Form(FormTemplate):
        def __init__(self, **properties):
            # You can do this in code or via the Designer:
            # - Designer: Drag a CheckBoxGroup onto your form, then drop CheckBoxes into it.
            # - Code: Create a CheckBoxGroup and add CheckBoxes as children.
            self.checkbox_group = CheckBoxGroup()
            self.add_component(self.checkbox_group)
            self.checkbox_group.add_component(CheckBox(text="Option A"))
            self.checkbox_group.add_component(CheckBox(text="Option B"))
            self.checkbox_group.add_event_handler("change", self.checkbox_group_change)

        def checkbox_group_change(self, **event_args):
            # Read the list of selected values
            print(self.checkbox_group.selected_values)  # -> ["Option A"] or ["Option A", "Option B"] etc.



Use the items property (like Dropdown)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``items`` may be a list of strings or a list of ``(text, value)`` tuples:

.. code-block:: python

    from anvil_extras import CheckBoxGroup

    # Simple list of strings: values equal the text
    self.checkbox_group = CheckBoxGroup(items=["One", "Two", "Three"])  # selected_values is a list of strings

    # List of (text, value) pairs: logical values are separate from the labels
    self.checkbox_group.items = [("Apples", "apples"), ("Oranges", "oranges"), ("Pears", "pears")]

    # Reading the selection returns a list of logical values (e.g. ["oranges", "pears"]):
    print(self.checkbox_group.selected_values)

    # Programmatic selection: set a list of logical values directly
    self.checkbox_group.selected_values = ["oranges", "pears"]  # checks "Oranges" and "Pears"


Group existing CheckBoxes on your form
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have individual ``CheckBox`` components on a form, you can group them:

.. code-block:: python

    from anvil_extras import CheckBoxGroup

    # If you already have CheckBoxes on your form (e.g. placed in the Designer),
    # you can add group behaviour without moving them into the CheckBoxGroup container.
    # The group provides a unified interface for reading/setting multiple selections
    # and consistent change events.
    self.checkbox_group = CheckBoxGroup()
    self.checkbox_group.checkboxes = [self.checkbox_1, self.checkbox_2]
    self.checkbox_group.add_event_handler("change", self.checkbox_group_change)

    # Alternatively, pass the checkboxes in the constructor
    self.checkbox_group = CheckBoxGroup(checkboxes=[self.checkbox_1, self.checkbox_2])
    self.checkbox_group.add_event_handler("change", self.checkbox_group_change)


Properties
----------

:selected_values: list[object]

    A list of the logical values of all checked options. When using ``items`` with ``(text, value)``
    pairs, this returns the ``value`` parts. When using a list of strings, these are the strings.
    Set to a list of matching values to programmatically select multiple options, or to ``[]`` to clear all.

:gap: string | float | int

    Spacing between checkboxes. Accepts a number (pixels) or a CSS length string
    (e.g. ``"12px"``, ``"0.5rem"``).

:spacing: spacing

    Standard Anvil container spacing

:direction: enum

    Layout direction of the group: ``"horizontal"`` (default) or ``"vertical"``.

:align: enum

    Alignment of checkboxes within the group. One of
    ``"left"``, ``"center"``, ``"right"``, ``"space-evenly"``, ``"space-between"``,
    ``"space-around"``. In horizontal layout this controls horizontal distribution;
    in vertical layout it controls cross-axis alignment.

:visible: bool

    Whether the component is visible.

:items: list[str] | list[tuple[str, Any]]

    Use to auto-generate checkboxes. Strings produce labels with the same value; tuples
    of ``(text, value)`` let you separate display text and logical value.

:checkboxes: list[anvil.CheckBox]

    Assign an explicit list of existing ``CheckBox`` components to be managed by
    the group. When set, event handlers are attached and the checkboxes are grouped for
    unified selection management. You can also provide this in the constructor,
    e.g. ``CheckBoxGroup(checkboxes=[cb1, cb2])``.


Events
------

:change:

    Fired when any checkbox selection changes. This is the default event. Use
    ``self.checkbox_group.selected_values`` inside the handler to read the current list of values.

:show:

    Fired when the component is shown.

:hide:

    Fired when the component is hidden.


Notes
-----

- When ``items`` contains ``(text, value)`` pairs, ``selected_values`` returns a list of
  the ``value`` parts; with a simple list of strings, it returns the strings themselves.
- Setting ``selected_values`` to values that don't exist will only select the matching ones.
- For tuple ``items``, set ``selected_values`` to a list of the tuples' logical values (e.g. ``["oranges", "pears"]``)
  at any time to select those options.
- ``align="left"``/``"right"`` map to flexbox ``flex-start``/``flex-end`` under the hood.
- To display checkboxes in a grid layout, use the ``style`` property:
  ``style="display: grid; grid-template-columns: repeat(3, 1fr);"`` for a 3-column grid.
