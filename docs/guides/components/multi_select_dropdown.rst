MultiSelectDropdown
===================
A multi select dropdown component with optional search bar


Overrides
---------

.. function:: format_selected_text(self, count, total)

    This method is called when the selection changes and should return a string.

    The default implementation looks like:

    .. code-block:: python

        from anvil_extras.MultiSelectDropDown import MultiSelectDropDown

        def format_selected_text(self, count, total):
            if count > 3:
                return f"{count} items selected"
            return ", ".join(self.selected_keys)


    You can change this by overriding this method.

    You can override it globally by doing the following

    .. code-block:: python

        from anvil_extras.MultiSelectDropDown import MultiSelectDropDown

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

:background: String

    Sets the button and popover background color. Note that this property only affects the basic button appearance and may not provide the visual consistency needed for complex themes. For more fine-grained control over all styling aspects including hover states, active states, and popover appearance, see the `Styling`_ section.

:foreground: String

    Sets the button text color. For more fine-grained control over all styling aspects including hover states, active states, and options appearance, see the `Styling`_ section.


Events
------
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


Styling
-------

The following CSS variables can be overridden in your theme.css to style the multi select dropdown.

**Button Styling:**

For button text and background colors and other styling, use CSS selectors to ensure proper cascade behavior:

.. code-block:: css

    /* Style the button directly using CSS selectors */
    .anvil-role-ae-ms-btn > button {
        color: #333333;
        background-color: #ffffff;
    }

    .anvil-role-ae-ms-btn > button:hover {
        color: #000000;
        background-color: #f8f9fa;
    }

    .anvil-role-ae-ms-btn > button:active:focus,
    .anvil-role-ae-ms-btn > button:focus,
    .anvil-role-ae-ms-btn > button:active {
        color: #000000;
        background-color: #e9ecef;
    }

**Note:** Avoid using CSS variables for text colors as they can override your global button styles. Use direct CSS selectors instead to maintain proper CSS cascade behavior.

**Option Styling:**

.. code-block:: css

    :root {
        /* Option text colors */
        --ae-ms-option-text: #333333;
        --ae-ms-option-text-active: #fff;

        /* Option background colors */
        --ae-ms-option-bg-hover: #e8e8e8;
        --ae-ms-option-bg-active: #337ab7;

        /* Subtext colors */
        --ae-ms-option-subtext: #777;
        --ae-ms-option-subtext-active: rgba(255,255,255,.5);
    }

**Popover Styling:**

The MultiSelectDropDown uses a popover with the class ``ae-ms-popover`` for specific targeting. You can style the popover background using CSS variables or direct CSS:

.. code-block:: css

    /* Target only MultiSelectDropDown popovers using CSS variables */
    .ae-popover.ae-ms-popover {
        --ae-popover-bg: #ffffff;
        --ae-popover-border: rgba(0, 0, 0, 0.2);
        --ae-popover-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    }

    /* Or style directly with CSS */
    .ae-popover.ae-ms-popover {
        background-color: #f8f9fa;
        color: #212529;
        border-color: #dee2e6;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

**CSS Roles:**

The following roles can be used for additional styling:

.. code-block:: css

    .anvil-role-ae-ms-btn {}
    .anvil-role-ae-ms-select-btn {}
    .anvil-role-ae-ms-filter {}
    .anvil-role-ae-ms-option {}
    .anvil-role-ae-ms-option-active {}
    .anvil-role-ae-ms-option-label {}
    .anvil-role-ae-ms-option-subtext {}

For general popover styling that affects all popovers, see the Popover styling guide.
