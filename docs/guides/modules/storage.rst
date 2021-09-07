Storage
=======

Introduction
------------
Browsers have a ``localStorage`` object that can store data between browser sessions

The anvil_extras :mod:`storage` module provides :const:`local_storage` object, which is a
convenient dictionary like wrapper around the native browser ``localStorage`` object.

The :attr:`local_storage` object can store data that persists accross browser sessions and is also available offline.
It could be used to create an entirely offline todo app, or to store simple data across sessions.

If access to the browser ``localStorage`` object is denied, :const:`local_storage` will
function as expected during the current session, but it will not be stored between browser
sessions, with a warning printed to the console indicating as much. Access may
be denied, for instance, if browser settings block third-party/cross-site cookies and the
app is being run within an 'iframe' (such as when clicking the "Run" button to test an
Anvil app in development mode).

(Browsers also have a ``sessionStorage`` object, and an equivalent :const:`session_storage`
object is also available in the :mod:`storage` module.)

Usage
-----

Store user preference
+++++++++++++++++++++

.. code-block:: python

    from anvil_extras.storage import local_storage

    class UserPreferences(UserPreferencesTemplate):
        def __init__(self, **properties):
            self.init_components(**properties)

        def dark_mode_checkbox_change(self, **event_args):
            local_storage['dark_mode'] = self.dark_mode_checkbox.checked


Change the theme at startup
+++++++++++++++++++++++++++

.. code-block:: python

    ## inside a startup module
    from anvil_extras.storage import local_storage

    if local_storage.get('dark_mode') is not None:
        # set the app theme to dark
        ...



API
---

.. object:: local_storage

   local_storage is a dictionary like object.

   .. describe:: list(local_storage)

      Return a list of all the keys used in :attr:`local_storage`.

   .. describe:: len(local_storage)

      Return the number of items in :attr:`local_storage`.

   .. describe:: local_storage[key]

      Return the item of :attr:`local_storage` with key *key*.  Raises a :exc:`KeyError` if *key* is
      not in :attr:`local_storage`. Raises a :exc:`TypeError` if *key* is not a string.

   .. describe:: local_storage[key] = value

      Set ``local_storage[key]`` to *value*. The *value* must be a json compatible object.

   .. describe:: del local_storage[key]

      Remove ``local_storage[key]`` from :attr:`local_storage`.

   .. describe:: key in local_storage

      Return ``True`` if :attr:`local_storage` has a key *key*, else ``False``.

   .. describe:: iter(local_storage)

      Return an iterator over the keys of the dictionary.  This is a shortcut
      for ``iter(local_storage.keys())``.

   .. method:: clear()

      Remove all items from the :attr:`local storage`.

   .. method:: get(key[, default])

      Return the value for *key* if *key* is in :attr:`local_storage`, else *default*.
      If *default* is not given, it defaults to ``None``, so that this method
      never raises a :exc:`KeyError`.

   .. method:: items()

      Return a map iterator of :attr:`local_storage`'s ``(key, value)`` pairs.

   .. method:: keys()

      Return a map iterator of :attr:`local storage`'s keys.

   .. method:: pop(key[, default])

      If *key* is in :attr:`local_storage`, remove it and return its value, else return
      *default*.  If *default* is not given, it defaults to ``None``, so that this method
      never raises a :exc:`KeyError`.

   .. method:: put(key, value)

      Equivalent to ``local_storage[key] = value``.

   .. method:: update([other])

      Update the :attr:`local_storage` with the key/value pairs from *other*, overwriting
      existing keys.  Return ``None``.

      :meth:`update` accepts either a dictionary object or an iterable of
      key/value pairs (as tuples or other iterables of length two).  If keyword
      arguments are specified, :attr:`local_storage` is then updated with those
      key/value pairs: ``local_storage.update(red=1, blue=2)``.

   .. method:: values()

      Return a map iterator of :attr:`local_storage`'s values.
