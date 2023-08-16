Autocomplete
============
A material design TextBox with autocomplete. A subclass of TextBox - other properties, events and methods inherited from TextBox.

Properties
----------

:suggestions: list[str]

    A list of autocomplete suggestions

:suggest_if_empty: bool

    If True then autocomplete will show all options when the textbox is empty

:filter_mode: "contains" | "startswith"

    contains: the autocomplete component will filter if a suggestion contains the search term.
    startswith: the autocomplete component will filter if a suggestions starts with the search term.

Events
------

:suggestion_clicked:

    When a suggestion is clicked. If a suggestion is selected with enter the ``pressed_enter`` event fires instead.
