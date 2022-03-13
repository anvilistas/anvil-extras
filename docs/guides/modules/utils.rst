Utils
=====
Client and server side utility functions.

Logging
-------

A lightweight logging implementation, similar to Python's logging module.
It can be used on both the server and the client.
It supports logging levels, and a custom format.

.. code-block:: python

    from anvil_extras.utils import logging

    user_logging = logger(name="user", level=logging.DEBUG, format="{name}-{level} {datetime:%Y-%m-%d %H:%M:%S}: {msg}")

    user_logging.info("user logging ready")
    # outputs 'user-INFO 2022-01-01 12:00:00: user logging ready'


API
^^^

.. class:: Logger(name="root", level=logging.INFO, format="{name}: {msg}", stream=sys.stdout)

    .. attribute:: name

        The name of the logger. Useful for distinguishing loggers in app logs.

    .. attribute:: level

        One of ``loging.NOTSET``, ``logging.DEBUG``, ``logging.INFO``, ``logging.WARNING``, ``logging.CRITICAL``
        If the logging level is set to ``logging.INFO``, then only logs at the level of
        ``INFO``, ``WARNING`` or ``CRITICAL`` will be logged. This is useful for turning on and off
        debug logs in your app.

    .. attribute:: format

        A format string. Valid options include ``name``, ``level``, ``msg``, ``datetime``, ``time``, ``date``.

    .. attribute:: stream

        A valid stream is any object that has a valid ``.write()`` and ``.flust()`` method.
        The default stream is the ``sys.stdout`` stream. This will log to the console in the IDE and passed to the app logs.
        A valid python stream can be used. On the client you may want to create your own.

    .. attribute:: disbaled

        To stop a logger from outputing to the console set it to disabled ``logger.disabled = True``.


    .. code-block:: python

        class CustomStream:
            def __init__(self, lbl):
                self.lbl = lbl

            def write(self, text):
                self.lbl.text += text

            def flush(self):
                pass

    .. method:: log(level, msg)

        The level is a valid logging level. If the level is greater than or equal to the logger's level
        the msg will be logged according to the loggers format.

    .. method:: debug(msg)

        Equivalent to ``logger.log(logging.DEBUG, msg)``

    .. method:: info(msg)

        Equivalent to ``logger.log(logging.INFO, msg)``

    .. method:: warning(msg)

        Equivalent to ``logger.log(logging.WARNING, msg)``

    .. method:: error(msg)

        Equivalent to ``logger.log(logging.ERROR, msg)``

    .. method:: critical(msg)

        Equivalent to ``logger.log(logging.CRITICAL, msg)``

    .. method:: get_format_params(*, level, msg, **params)

        This method can be overridden by subclass. Any extra params can be used in the format string.

    .. code-block:: python

        class TimerLogger(Logger):
            def get_format_params(self, *, level, msg, **params):
                elapsed = time.time() - self.curr_time
                return super().get_format_params(level=level, msg=msg, elapsed=elapsed, **params)



Timing
------

TimerLogger
^^^^^^^^^^^

The ``TimerLogger`` is a subclass of ``Logger``.
It supports an extra format argument ``elapsed`` with a default format of:
``"{time:%H:%M:%S} | {name}: ({elapsed:6.3f} secs) | {msg}"``

It adds 3 methods which can be used as follows.

.. code-block:: python

    from anvil_extras.utils.logging import TimerLogger
    from time import sleep

    T = TimerLogger("my timer")
    T.start("starting") # optional msg
    sleep(1)
    T.check("first check") # optional msg
    sleep(3)
    T.check("second check", restart=True) # restarts the timer
    sleep(2)
    T.end() # optional msg - ends the timer

The above code logs

.. code-block:: python

    # 20:57:56 | my timer: ( 0.000 secs) | starting
    # 20:57:57 | my timer: ( 1.012 secs) | first check
    # 20:58:00 | my timer: ( 4.020 secs) | second check (restart)
    # 20:58:02 | my timer: ( 2.005 secs) | end


Each method can take an option msg argument.
Each method calls the the ``debug()`` method, i.e. if you set ``TimerLogger(level=logging.INFO)``,
then the above logs would not be displayed in the console.

A ``TimerLogger`` can also be used with a ``with`` statement.

.. code-block:: python

    from anvil_extras.utils.logging import TimerLogger
    from time import sleep

    def foo():
        with TimerLogger("timing foo") as T:
            sleep(1)
            T.check("first check")
            sleep(3)
            T.check("second check", restart=True)
            sleep(2)

When used as a context manager the ``TimerLogger`` will call the ``.start()`` and ``.end()`` method.

The ``TimerLogger`` can also be used as a convenient decorator.

.. code-block:: python



    from anvil_extras.utils.logging import TimerLogger
    from time import sleep

    @TimerLogger("foo timer")
    def foo():
        ...

    foo()

    # 21:12:47 | foo: ( 0.000 secs) | start
    # 21:12:48 | foo: ( 1.014 secs) | end

For a more detailed timing decorator use ``anvil_extras.utils.timed`` decorator.


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
On the server this can be from the Python ``logging`` module.

The decorator also takes an optional ``level`` keyword argument which must be one of the standard levels from the logging module.
When no argument is passed, the default level is ``logging.INFO``.

The default logger is an anvil_extras Logger instance, which will log to stdout.
Messages will appear in your App's logs and in the IDE console.
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

Now, the form has an ``item`` property which behaves like a dictionary. Whenever a value of that dictionary changes, the form's ``refresh_data_bindings`` method will be called.

Note: The ``item`` property will no longer reference the same object. Rather, in the following example, it is as though auto-refresh adds the ``item = dict(item)`` line:

.. code-block:: python

   other_item = {"x": 1}
   item = other_item

   item = dict(item)
   item["x"] = 2

As in the above code, with auto-refresh, ``item`` is changed but ``other_item`` is not.


Wait for writeback
------------------
Using ``wait_for_writeback`` as a decorator prevents a function executing before any queued writebacks have completed.

This is particularly useful if you have a form with text fields. Race condidtions can occur between a text field writing back to an item and a click event that uses the item.

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
