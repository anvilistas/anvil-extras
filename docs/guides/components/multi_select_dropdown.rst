MultiSelectDropdown
===================
A multi select dropdown component with optional search bar


Overrides
---------

.. function:: format_selected_text(self, count, total)

    This method is called when the selection changes and should return a string.

    The default implementation looks like:

    .. code-block:: python

        from anvil_extras import MultiSelectDropdown

        def format_selected_text(self, count, total):
            if count > 3:
                return f"{count} items selected"
            return ", ".join(self.selected_keys)


    You can change this by overriding this method.

    You can override it globally by doing the following

    .. code-block:: python

        from anvil_extras import MultiSelectDropdown

        def format_selected_text(self, count, total):
            if count > 2:
                return f"{count} items selected of {total}"
            return ", ".join(self.selected_keys)

        MultiSelectDropdown.format_selected_text = format_selected_text


    Alternatively you can change the ``count_selected_text`` method per multiselect instance

    .. code-block:: python

        class Form1(Form1Template):
            def __init__(self, **properties):
                ...

                def format_selected_text(count, total):
                    if count > 3:
                        return f"{count} items selected"
                    return ", ".join(self.multi_select_drop_down_1.selected_keys)

                self.multi_select_drop_down_1.format_selected_text = format_selected_text



Properties
----------
:align: String

    ``"left"``, ``"right"``, ``"center"``

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

:width: String | Number

    The default width is 200px. This can be set using any css length.
    Alternatively set the width to be ``"auto"``, which will adjust the width to be as wide as the largest option.
    ``"fit"`` (or ``"fit-content"``) will size the dropdown depending on what is selected.
    Use width ``"100%""`` to make the dropdown fill its container.

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

:opened:

    When the dropdown is opened

:closed:

    When the dropdown is closed

:show:

    When the component is shown

:hide:

    When the component is hidden
