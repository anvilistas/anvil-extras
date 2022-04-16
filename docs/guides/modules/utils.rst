Utils
=====
Client and server-side utility functions.




import_module
-------------

Very similar to python's ``importlib.import_module`` implementation.
Use in the same way.

Takes two arguments, the ``name`` to import, and an optional ``package``.

The 'package' argument is required when performing a relative import. It
specifies the package to use as the anchor point from which to resolve the
relative import to an absolute import.


**Example implementation:**

.. code-block:: python

    from anvil_extras.utils import import_module
    from functools import cache

    class MainForm(MainFormTemplate):
        ...

        def link_click(self, sender, **event_args):
            self.load_form(sender.tag)

        @cache
        def get_form(self, form_name):
            form_module = import_module(f".{form_name}", __package__)
            form_cls = getattr(form_module, form_name)
            return form_cls()


        def load_form(self, form_name):
            form = self.get_form(form_name)
            self.content_panel.clear()
            self.content_panel.add_component(form)


Timing
------


timed decorator
^^^^^^^^^^^^^^^

Import the ``timed`` decorator and apply it to a function:

.. code-block:: python

   import anvil.server
   from anvil_extras.utils import timed


   @anvil.server.callable
   @timed
   def target_function(args, **kwargs):
       print("hello world")

The decorator takes a ``logging.Logger`` instance as one of its optional keyword arguments.
On both the server and the client this can be a Logger from the anvil_extras logging module.
On the server, this can be from the Python ``logging`` module.

The decorator also takes an optional ``level`` keyword argument which must be one of the standard levels from the logging module.
When no argument is passed, the default level is ``logging.INFO``.

The default logger is an anvil_extras Logger instance, which will log to stdout.
Messages will appear in your App's logs and the IDE console.
You can, however, create your own logger and pass that instead if you need more sophisticated behaviour:

.. code-block:: python

   import logging
   from anvil_extras.utils import timed

   my_logger = logging.getLogger(__name__)


   @timed(logger=my_logger, level=logging.DEBUG)
   def target_function(args, **kwargs):
       ...

.. code-block:: python

   from anvil_extras.utils import timed, logging

   my_logger = logging.Logger(name="Timing", format={"{name}: {time:%H:%M:%S}-{msg}"}, level=logging.DEBUG)

   @timed(logger=my_logger, level=logging.DEBUG)
   def target_function(args, **kwargs):
       ...



Auto-Refresh
------------
Whenever you set a form's ``item`` attribute, the form's ``refresh_data_bindings`` method is called automatically.

The ``utils`` module includes a decorator you can add to a form's class so that ``refresh_data_bindings`` is called whenever ``item`` changes at all.

To use it, import the decorator and apply it to the class for a form:

.. code-block:: python

   from anvil_extras.utils import auto_refreshing
   from ._anvil_designer import MyFormTemplate


   @auto_refreshing
   class MyForm(MyFormTemplate):
       def __init__(self, **properties):
           self.init_components(**properties)

The form's ``item`` property will be proxied.

If your original item was a dictionary, whenever a value of the proxied item changes,
the form's ``refresh_data_bindings`` method will be called.

Note that the proxied item will make changes to the original ``item``.

It shouldn't matter what the original ``item`` is. It could be a dictionary, app_table Row or some other obsucre object.


Wait for writeback
------------------
Using ``wait_for_writeback`` as a decorator prevents a function from executing before any queued writebacks have been completed.

This is particularly useful if you have a form with text fields. Race conditions can occur between a text field writing back to an item and a click event that uses the item.

To use ``wait_for_writeback``, import the decorator and apply it to a function, usually an event_handler:

.. code-block:: python

   from anvil_extras.utils import wait_for_writeback

   class MyForm(MyFormTemplate):
        ...

        @wait_for_writeback
        def button_1_click(self, **event_args):
            anvil.server.call("save_item", self.item)


The click event will now only be called after all active writebacks have finished executing.


Correct Canvas Resolution
-------------------------

Canvas elements can appear blurry on retina screens.
This helper function ensures a canvas element appears sharp.
It should be called inside the canvas ``reset`` event.

.. code-block:: python

   from anvil_extras.utils import correct_canvas_resolution

   class MyForm(MyFormTemplate):
        ...

        def canvas_reset(self, **event_args):
            c = self.canvas
            correct_canvas_resolution(c)
            ...
