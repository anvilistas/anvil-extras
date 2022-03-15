MultiSelectDropdown
===================
A multi select dropdown component with optional search bar

Properties
----------
:align: String

    ``"left"``, ``"right"``, ``"center"`` or ``"full"``

:items: Iterable of Strings, Tuples or Dicts

    Strings and tuples as per Anvil's native dropdown component. More control can be added by setting the items to a list of dictionaries.
    e.g.

    .. code-block:: python

        self.multi_select_drop_down.items = [
            {"key": "1st", "value": 1, "subtext": "pick me"},
            {"key": "2nd", "value": 2, "enabled": False},
            "---",
            {"key": "item 3", "value": 3, "title": "3rd times a charm"},
        ]

    The ``"key"`` property is what is displayed in the dropdown.
    The ``value`` property is what is returned from the ``selected_values``.

    The remainder of the properties are optional.

    ``"enabled"`` determines if the option is enabled or not - defaults to ``True``.

    ``"title"`` determines what is displayed in the selected box - if not set it will use the value from ``"key"``.

    ``"subtext"`` adds subtext to the dropdown display.

    To create a divider include ``"---"`` at the appropriate index.

:placeholder: String

    Placeholder when no items have been selected

:enable_filtering: Boolean

    Allow searching of items by key

:multiple: Boolean

    Can also be set to false to disable multiselect

:enabled: Boolean

    Disable interactivity

:visible: Boolean

    Is the component visible

:spacing_above: String

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:spacing_below: String

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:selected: Object

    get or set the current selected values.

:enable_select_all: Boolean

    Enable Select All and Deselect All buttons.


Events
----------
:change:

    When the selection changes

:show:

    When the component is shown

:hide:

    When the component is hidden
