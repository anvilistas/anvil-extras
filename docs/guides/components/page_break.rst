PageBreak
=========
For use in forms which are rendered to PDF to indicate that a page break is required.

The optional ``margin_top`` property  changes the amount of white space at the top of the page.
You can set the ``margin_top`` property to a positive/negative number to adjust the whitespace.
Most of the time this is unnecessary. This won't have any effect on the designer, only the generated PDF.

The optional ``border`` property defines the style of the component in the IDE.
The value of the property affects how a ``PageBreak`` component looks in the browser during the execution.
It has no effect in the generated PDF, where the component is never visible or in the IDE, where the component
is always ``"1px solid grey"``.

It is possible to change the default style for all the ``PageBreak``\ s in the app by adding the following code to ``theme.css``:

.. code-block:: css

    .break-container {
        border: 2px dashed red !important;
    }

Using this technique rather than the ``border`` property affects how the component looks both in the IDE and at runtime.
