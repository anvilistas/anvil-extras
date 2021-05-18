MultiSelectDropdown
============
A multi select dropdown component with optional search bar

Properties
----------
:align: String

    "left", "right", "center" or "full"

:items: Object

    Can be use a list of stings or a list of tuples, (str, value) pairs. Or a list of dicts with keys: "key",
    "value, "icon", "title", "enabled"

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

    One of "none", "small", "medium", "large"

:spacing_below: String

    One of "none", "small", "medium", "large"

:selected: Object

    get or set the current selected values.


Events
----------
:change:

    When the selection changes

:show:

    When the component is shown

:hide:

    When the component is hidden
