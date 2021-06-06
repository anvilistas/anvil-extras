Chip
=====
A variation on a label that includes a close icon. Largely based on the Material design Chip component.

Properties
----------

:text: str

    Displayed text

:icon: icon

    Can be a font awesome icon or a media object

:close_icon: boolean

    Whether to include the close icon or not

:foreground: color
    the color of the text and icons

:background: color
    background color for the chip

:spacing_above: str

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:spacing_below: str

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:visible: bool

    Is the component visible



Events
------
:close_click:

    When the close icon is clicked

:click:

    When the chip is clicked

:show:

    When the component is shown

:hide:

    When the component is hidden




ChipsInput
==========
A component for adding tags/chips. Uses a Chip with no icon.

Properties
----------

:chips: tuple[str]

    the text of each chip displayed. Empty strings will be ignored, as will duplicates.

:primary_placeholder: str

    The placeholder when no chips are displayed

:secondary_placeholder: str

    The placeholder when at least one chip is displayed

:spacing_above: str

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:spacing_below: str

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:visible: bool

    Is the component visible


Events
------
:chips_changed:

    When a chip is added or removed

:chip_added:

    When a chip is added. Includes the chip text that was added as an event arg.

:chip_removed:

    When a chip is removed. Includes the chip text that was removed as an event arg;

:show:

    When the component is shown

:hide:

    When the component is hidden
