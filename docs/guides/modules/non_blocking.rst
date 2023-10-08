NonBlocking
===========

Call functions in a non-blocking way.

In a blocking execution, the next line of code
will not be executed until the current line has completed.

In contrast, non-blocking execution allows the next line
to be executed without waiting for the current line to complete.

.. note::

   This module cannot be used to call server functions simultaneously, as Anvil server calls are queued.

A suitable use case for this library is when you want to perform an action without waiting for a response,
such as updating a database after making changes on the client side.


Examples
--------

Call a server function
**********************

After updating the client, call a server function to update the database.
In this example, we don't care about the return value.

.. code-block:: python

    from anvil_extras.non_blocking import call_async

    def button_click(self, **event_args):
        self.update_database()
        self.open_form("Form1")

    def update_database(self):
        # Unlike anvil.server.call, we do not wait for the call to return
        call_async("update", self.item)


Handle return values and errors
*******************************

If you want to handle the return value or any errors,
you can provide result and error handlers.

.. code-block:: python

    from anvil_extras.non_blocking import call_async

    def handle_result(self, res):
        print(res)
        Notification("successfully saved").show()

    def handle_error(self, err):
        print(err)
        Notification("there was a problem", style="danger").show()

    def update_database(self, **event_args):
        call_async("update", self.item).on_result(self.handle_result, self.handle_error)
        # Equivalent to
        async_call = call_async("update", self.item)
        async_call.on_result(self.handle_result, self.handle_error)
        # Equivalent to
        async_call = call_async("update", self.item)
        async_call.on_result(self.handle_result)
        async_call.on_error(self.handle_error)


repeat
******

Call a function repeatedly using the ``repeat()`` function.
The function will be called after each specified interval in seconds.
To end or cancel the repeated call, use the ``cancel`` method.

.. code-block:: python

    from anvil_extras import non_blocking

    i = 0
    def do_heartbeat():
        global heartbeat, i
        if i >= 42:
            heartbeat.cancel()
            # equivalent to non_blocking.cancel(heartbeat)
        print("da dum")
        i += 1

    heartbeat = non_blocking.repeat(do_heartbeat, 1)


defer
*****

Call a function after a set period of time using the ``defer()`` function.
To cancel the deferred call, use the ``cancel()`` method.

.. code-block:: python

    from anvil_extras import non_blocking

    class Form1(Form1Template):
        def __init__(self, **properties):
            ...
            self.deferred_search = None

        def update_search_results(self):
            search_results = anvil.server.call_s("search_results", self.search_box.text)
            # do something with search_results

        def search_box_change(self, **event_args):
            # cancel the existing deferred_search
            non_blocking.cancel(self.deferred_search)
            self.deferred_search = non_blocking.defer(self.update_search_results, 0.3)


In this example we call ``self.update_search_results()`` only when the user has stopped typing for 0.3 seconds.
If the user starts typing again before 0.3 seconds is up, the deferred call is cancelled.
This prevents us calling the server too often.



API
---

.. function:: call_async(fn, *args, **kws)
              call_async(fn_name, *args, **kws)

    Returns an ``AsyncCall`` object. The *fn* will be called in a non-blocking way.

    If the first argument is a string, then the server function with the name *fn_name* will be called in a non-blocking way.

.. function:: wait_for(async_call_object)

    Blocks until the ``AsyncCall`` object has finished executing.

.. class:: AsyncCall

    Don't instantiate this class directly; instead, use the functions above.

    .. method:: on_result(self, result_handler, error_handler=None)

        Provide a result handler to handle the return value of the non-blocking call.
        Provide an optional error handler to handle the error if the non-blocking call raises an exception.
        Both handlers should take a single argument.

        Returns ``self``.

    .. method:: on_error(self, error_handler)

        Provide an error handler that will be called if the non-blocking call raises an exception.
        The handler should take a single argument, the exception to handle.

        Returns ``self``.

    .. method:: await_result(self)

        Waits for the non-blocking call to finish executing and returns the result.
        Raises an exception if the non-blocking call raised an exception.

    .. property:: result

        If the non-blocking call has not yet completed, raises a ``RuntimeError``.

        If the non-blocking call has completed, returns the result.
        Raises an exception if the non-blocking call raised an exception.

    .. property:: error

        If the non-blocking call has not yet completed, raises a ``RuntimeError``.

        If the non-blocking call raised an exception, the exception raised can be accessed using the ``error`` property.
        The error will be ``None`` if the non-blocking call returned a result.

    .. property:: status

        One of ``"PENDING"``, ``"FULFILLED"``, ``"REJECTED"``.

    .. property:: promise

        Returns a JavaScript Promise that resolves to the value from the function call



.. function:: cancel(ref)

    Cancel an active call to ``delay`` or ``defer``.
    The first argument should be ``None`` or the return value from a call to ``delay`` or ``defer``.

    Calling ``cancel(ref)`` is equivalent to ``ref.cancel()``.
    You may wish to use ``cancel(ref)`` if you start with a placeholder ``ref`` equal to ``None``.
    See the ``defer`` example above.

.. function:: repeat(fn, interval)

    Repeatedly call a function with a set interval (in seconds).

    - ``fn`` should be a callable that takes no arguments.
    - ``interval`` should be an ``int`` or ``float`` representing the time in seconds between function calls.

    The function is called in a non-blocking way.

    A call to ``repeat`` returns a ``RepeatRef`` object that has a ``.cancel()`` method.

    Calling the ``.cancel()`` method will stop the next repeated call from executing.

.. function:: defer(fn, delay)

    Defer a function call after a set period of time has elapsed (in seconds).

    - ``fn`` should be a callable that takes no arguments.
    - ``delay`` should be an ``int`` or ``float`` representing the time in seconds.

    The function is called in a non-blocking way.
    A call to ``defer`` returns a ``DeferRef`` object that has a ``.cancel()`` method.

    Calling the ``.cancel()`` method will stop the deferred function from executing.
