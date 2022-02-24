Quill Editor
============
A wrapper around the Quill editor.

Properties
----------

:auto_expand: Boolean

    When set to ``True`` the Editor will expand with the text. If ``False`` the height is the starting height.

:content: Object

    This returns a list of dicts. The content of any Quill editor is represented as a Delta object. A Delta object is a wrapper around a JSON object that describes the state of the Quill editor. This property exposes the undelrying JSON which can then be stored in a data table simple object cell.

    When you do ``self.quill.content = some_object``, this will call the underlying ``setContents()`` method.

    You can also set the ``content`` property to a string. This will call the underlying ``setText()`` method.

    Retrieving the ``content`` property will always return the underlying JSON object that represents the contents of the Quill editor. It is equivalent to ``self.quill.getContents().ops``.

:enabled: Boolean

    Disable interactivity

:height: String

    With auto_expand this becomes the starting height. Without auto_expand this becomes the fixed height.

:modules: Object

    Additional modules can be set at runtime. See Quill docs for examples. If a toolbar option is defined in modules this will override the toolbar property.

:placeholder: String

    Placeholder when there is no text

:readonly: Boolean

    Check the Quill docs.

:sanitize: Boolean

    Set the default sanitize behaviour used for the ``set_html()`` method.

:spacing_above: String

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:spacing_below: String

    One of ``"none"``, ``"small"``, ``"medium"``, ``"large"``

:theme: String

    Quill supports ``"snow"`` or ``"bubble"`` theme.

:toolbar: Boolean or Object

    Check the Quill docs. If you want to use an Object you can set this at runtime. See quill docs for examples.

:visible: Boolean

    Is the component visible


Methods
----------
All the methods from the Quill docs should work. You can use camel case or snake case. For example ``self.quill.get_text()`` or ``self.quill.getText()``. These will not come up in the autocomplete.

Methods from the Quill docs call the underlying javascript Quill editor and the arguments/return values will be as described in the Quill documentation.

There are two Anvil specific methods:

:get_html:

    Returns a string representing the html of the contents of the Quill editor. Useful for presenting the text in a RichText component under the ``"restricted_html"`` format.

:set_html(html, sanitize=None):

    Set the contents of the Quill editor to html.
    If ``sanitize`` is ``True``, then the html will be sanitized in the same way that a RichText component sanitizes the html.
    If ``sanitize`` is unset the the default ``sanitize`` attribute will be used to determine this behaviour.
    If See Anvil's documentation on the RichText component.




Events
----------
:text_change:

    When the text changes

:selection_change:

    When the selection changes

:show:

    When the component is shown

:hide:

    When the component is hidden
