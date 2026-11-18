Virtualizer
===========

Use ``Virtualizer`` to render a long list without creating a DOM node for
every item. It wraps TanStack Virtual and is used by MultiSelectDropDown
and Autocomplete. It is a client-side helper, so you supply the row markup
and the data. It does not fetch more records or behave as a RepeatingPanel.

Example: 10,000 records
-----------------------

Add Anvil Extras as a dependency (this example uses v3.6.3). Create an HTML
Form called ``Demo``, set it as the startup Form, and paste the following into
its HTML and Python editors.

The viewport has a bounded height, and the relative inner canvas is as tall
as the full list. Each rendered row is positioned at the offset returned by
the virtualizer. The count above the viewport shows how many DOM nodes exist.

Demo HTML
~~~~~~~~~

.. code-block:: html

   <main style="max-width: 42rem; margin: 2rem auto; padding: 0 1rem;">
     <h1>Anvil Extras Virtualizer</h1>
     <p>Scroll through 10,000 records. Only the nearby DOM rows are rendered.</p>
     <p anvil:dom-node="status"></p>
     <div anvil:dom-node="viewport" tabindex="0" role="region"
          aria-label="Records" style="height: 20rem; overflow: auto; border: 1px solid #888;">
       <div anvil:dom-node="canvas" style="position: relative;"></div>
     </div>
   </main>

Demo Python
~~~~~~~~~~~

.. code-block:: python

   from anvil import handle
   from anvil.js.window import document
   from anvil_extras.virtualize import Virtualizer

   from ._anvil_designer import DemoTemplate

   ROW_HEIGHT = 40


   class Demo(DemoTemplate):
       def __init__(self, **properties):
           self.init_components(**properties)
           self.records = [f"Record {i:,}" for i in range(1, 10_001)]
           self.virtualizer = Virtualizer(
               count=len(self.records),
               component=self,
               scroll_element=self.dom_nodes["viewport"],
               estimate_size=lambda index: ROW_HEIGHT,
               on_change=self.render_window,
           )

       @handle("", "show")
       def shown(self, **event_args):
           self.render_window()

       def render_window(self):
           canvas = self.dom_nodes["canvas"]
           canvas.replaceChildren()
           canvas.style.height = f"{self.virtualizer.get_total_size()}px"

           for item in self.virtualizer.get_virtual_items():
               row = document.createElement("div")
               row.textContent = self.records[item.index]
               row.setAttribute(
                   "style",
                   "position:absolute; inset-inline:0; box-sizing:border-box;"
                   "padding:8px 12px; border-bottom:1px solid #ccc;"
                   f"top:{item.start}px; height:{ROW_HEIGHT}px;",
               )
               canvas.appendChild(row)

           self.dom_nodes["status"].textContent = (
               f"{canvas.childElementCount} DOM rows / {len(self.records):,} records"
           )

How it works
------------

* ``component`` owns the mount lifecycle. The helper listens for the Anvil
  page-added and page-removed events to start and clean up its observers.
* ``estimate_size(index)`` returns the row height in pixels. This example
  makes every row exactly that height. The wrapper does not measure
  arbitrary row content.
* ``on_change`` is called without arguments. Use ``get_virtual_items()``
  to get the visible window and nearby rows. Each item has an ``index``
  into your data and a ``start`` offset in pixels.
* When data changes, update your records, call ``update(count=len(records))``
  and render again. Pass ``get_item_key`` if indices are not stable.
  Use ``scroll_to_index(index)`` to reveal a specific row.
* For server paging, fetch another batch separately when the window
  approaches the end of the loaded records, then update the count.

For a working component implementation, see the
`MultiSelectDropDown render method <https://github.com/anvilistas/anvil-extras/blob/7a3e625c5d2983323442edb321f3380bd24e8504/client_code/MultiSelectDropDown/DropDown/__init__.py#L430-L451>`_.
