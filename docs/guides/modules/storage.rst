Storage
=======

Introduction
------------
Browsers have various ways to store data. ``localStorage`` and ``indexedDB`` are two such storage mechanisms that are particularly useful for storing data offline.

The anvil_extras :mod:`storage` module provides both a :attr:`local_storage` object and a :attr:`indexed_db` object, which are
convenient dictionary like wrappers around the native browser objects.

The :attr:`local_storage` and :attr:`indexed_db` objects can store data that persists accross browser sessions and are also available offline.
It could be used to create an entirely offline todo app, or to store data across sessions.

Note that when working in the IDE the app is running in an IFrame and the ``storage`` objects may not be available. This can be fixed by changing your browser settings.
Turning the shields down in Brave or making sure not to block third party cookies in Chrome should fix this.


Which to chose?
+++++++++++++++
If you have small amounts of data which can be converted to JSON then use the :attr:`local_storage` object.
If you have more data which can be converted to JSON (and also ``bytes`` objects) - use :attr:`indexed_db`.


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

.. class:: StorageWrapper()

   both :attr:`indexed_db` and :attr:`local_storage` are instances of a dictionary like :class:`StorageWrapper` class.

   .. describe:: is_available()

      Check if the storage object is supported. Returns a ``boolean``.

   .. describe:: get_store(name)

      Get or create a ``storage`` object. e.g. ``todo_store = indexed_db.get_store('todos')``. This will create a new storage object inside the browser's ``IndexedDB``.
      The :attr:`indexed_db` object is equivalent to ``indexed_db.get_store('default')``. To explore this further, open up devtools and find ``IndexedDB`` in the Application tab.

   .. describe:: list(store)

      Return a list of all the keys used in the *store*.

   .. describe:: len(store)

      Return the number of items in *store*.

   .. describe:: store[key]

      Return the item of *store* with key *key*.  Raises a :exc:`KeyError` if *key* is
      not in *store*. Raises a :exc:`TypeError` if *key* is not a string.

   .. describe:: store[key] = value

      Set ``store[key]`` to *value*. If the value is not a JSONable data type it may be stored incorrectly. e.g. a ``datetime`` object.
      If storing ``bytes`` objects it is best to use the :attr:`indexed_db` store.

   .. describe:: del store[key]

      Remove ``store[key]`` from *store*.

   .. describe:: key in store

      Return ``True`` if *store* has a key *key*, else ``False``.

   .. describe:: iter(store)

      Return an iterator over the keys of the *store*.  This is a shortcut
      for ``iter(store.keys())``.

   .. method:: clear()

      Remove all items from the :attr:`local storage`.

   .. method:: get(key[, default])

      Return the value for *key* if *key* is in *store*, else *default*.
      If *default* is not given, it defaults to ``None``, so that this method
      never raises a :exc:`KeyError`.

   .. method:: items()

      Return a map iterator of *store*'s ``(key, value)`` pairs.

   .. method:: keys()

      Return a map iterator of :attr:`local storage`'s keys.

   .. method:: pop(key[, default])

      If *key* is in *store*, remove it and return its value, else return
      *default*.  If *default* is not given, it defaults to ``None``, so that this method
      never raises a :exc:`KeyError`.

   .. method:: put(key, value)

      Equivalent to ``store[key] = value``.

   .. method:: update([other])

      Update the *store* with the key/value pairs from *other*, overwriting
      existing keys.  Return ``None``.

      :meth:`update` accepts either a dictionary object or an iterable of
      key/value pairs (as tuples or other iterables of length two).  If keyword
      arguments are specified, *store* is then updated with those
      key/value pairs: ``store.update(red=1, blue=2)``.

   .. method:: values()

      Return a map iterator of *store*'s values.
