Logging
=======

A lightweight logging implementation, similar to Python's logging module.
It can be used on both the server and the client.
It supports logging levels and a custom format.

Logger
------

.. code-block:: python

    from anvil_extras.logging import Logger, DEBUG

    user_logging = Logger(
        name="user",
        level=DEBUG,
        format="{name}-{level} {datetime:%Y-%m-%d %H:%M:%S}: {msg}",
    )

    user_logging.info("user logging ready")
    # outputs 'user-INFO 2022-01-01 12:00:00: user logging ready'


API
^^^

.. class:: Logger(name="root", level=logging.INFO, format="{name}: {msg}", stream=sys.stdout)

    .. attribute:: name

        The name of the logger. Useful for distinguishing loggers in app logs.

    .. attribute:: level

        One of ``logging.NOTSET``, ``logging.DEBUG``, ``logging.INFO``, ``logging.WARNING``, ``logging.CRITICAL``
        If the logging level is set to ``logging.INFO``, then only logs at the level of
        ``INFO``, ``WARNING`` or ``CRITICAL`` will be logged. This is useful for turning on and off
        debug logs in your app.

    .. attribute:: format

        A format string. Valid options include ``name``, ``level``, ``msg``, ``datetime``, ``time``, ``date``.

    .. attribute:: stream

        A valid stream is any object that has a valid ``.write()`` and ``.flust()`` method.
        The default stream is the ``sys.stdout`` stream. This will log to the console in the IDE and get passed to the app logs.
        A valid python stream can be used. On the client, you may want to create your own.

    .. attribute:: disabled

        To stop a logger from outputting to the console set it to disabled ``logger.disabled = True``.


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
        the msg will be logged according to the logger's format.

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

        This method can be overridden by a subclass. Any extra params can be used in the format string.

    .. code-block:: python

        class TimerLogger(Logger):
            def get_format_params(self, **params):
                elapsed = time.time() - self.curr_time
                return super().get_format_params(elapsed=elapsed, **params)

        # with UID

        from anvil_extras.uuid import uuid4

        class UIDLogger(Logger):
            def __init__(self, name="uid logger", uid=None, level=INFO, format="{uid}: {msg}"):
                super().__init__(name=name, level=level, format=format)
                self.uid = uid or uuid4()

            def get_format_params(self, **params):
                return super().get_format_params(uid=self.uid, **params)


TimerLogger
-----------

The ``TimerLogger`` is a subclass of ``Logger`` and allows for debug timing in various ways.
It supports an extra format argument ``elapsed``.
The default format for a ``TimerLogger`` is:
``"{time:%H:%M:%S} | {name}: ({elapsed:6.3f} secs) | {msg}"``

It adds 3 methods to the API above:

.. method:: start(msg='start')

    records the starting timestamp

.. method:: check(msg="check", restart=False)

    records the elapsed time (optionally restart the ``TimerLogger``)

.. method:: end(msg="end")

    records the elapsed time and ends the ``TimerLogger``


The ``TimerLogger`` can be used to check times between lines of code.

.. code-block:: python

    from anvil_extras.logging import TimerLogger
    from time import sleep

    T = TimerLogger("my timer")
    T.start("starting") # optional msg
    sleep(1)
    T.check("first check") # optional msg
    sleep(3)
    T.check("second check", restart=True) # restarts the timer
    sleep(2)
    T.end() # optional msg - ends the timer

The above code logs:

.. code-block:: python

    # 20:57:56 | my timer: ( 0.000 secs) | starting
    # 20:57:57 | my timer: ( 1.012 secs) | first check
    # 20:58:00 | my timer: ( 4.020 secs) | second check (restart)
    # 20:58:02 | my timer: ( 2.005 secs) | end


Each method can take an optional msg argument.
Each method calls the the ``.debug()`` method, i.e. if you set ``TimerLogger(level=logging.INFO)``,
then the above logs would not be displayed in the console.

A ``TimerLogger`` can be used with a ``with`` statement (as a context manager).

.. code-block:: python

    from anvil_extras.logging import TimerLogger
    from time import sleep

    def foo():
        with TimerLogger("timing foo") as T:
            sleep(1)
            T.check("first check")
            sleep(3)
            T.check("second check", restart=True)
            sleep(2)

When used as a context manager the ``TimerLogger`` will call the ``.start()`` and ``.end()`` method.

The ``TimerLogger`` can be used as a convenient decorator.

.. code-block:: python

    from anvil_extras.logging import TimerLogger
    from time import sleep

    @TimerLogger("foo timer")
    def foo():
        ...

    foo()

    # 21:12:47 | foo timer: ( 0.000 secs) | start
    # 21:12:48 | foo timer: ( 1.014 secs) | end

For a more detailed timing decorator use ``anvil_extras.utils.timed`` decorator.
