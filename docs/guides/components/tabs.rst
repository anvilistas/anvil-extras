Tabs
============
A simple way to implement tabs. Works well above another container abover or below. Set the container spacing property to none.
It also understand the role material design role ``'card'``

Properties
----------

:tab_titles: list[str]

    The titles of each tab.

:active_tab_index: int

    Which tab should be active.

:foreground: color
    the color of the highlight and text. Defaults to ``"theme:Primary 500"``

:background: color
    the background for all tabs. Defaults to ``"transparent"``

:role:
    set the role to ``'card'`` or create your own role

:align: str

    ``"left"``, ``"right"``, ``"center"`` or ``"full"``

:bold: bool

    applied to all tabs

:italic: bool

    applied to all tabs

:font_size: int

    applied to all tabs

:font: str

    applied to all tabs

:visible: Boolean

    Is the component visible

:spacing_above: String

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:spacing_below: String

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``


Events
----------
:tab_click:

    When any tab is clicked. Includes the parameters ``tab_index`` ``tab_title`` and ``tab_component`` as part of the ``event_args``

:show:

    When the component is shown

:hide:

    When the component is hidden
