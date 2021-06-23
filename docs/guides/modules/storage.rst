:mod:`storage` --- wrapper around window.Storage
================================================


Introduction
------------
Browsers have a localStorage and a sessionStorage object.
The browser localStorage object persists between browser sessions, where the sessionStorage object does not.

The :object:`local_storage` object provides a convenient dictionary like wrapper around the javacript localStorage object.
Similary the :object:`session_storage` provides a wrapper around the sessionStorage object.


The :object:`local_storage` object is also available offline and may be convenient for storing data.
For example - it could be used to create an entirely offline todo app, or to store simple data across sessions.


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



local_storage
-------------

.. object:: local_storage

   local_storage is a dictionary like object.

   .. describe:: list(local_storage)

      Return a list of all the keys used in :object:`local_storage`.

   .. describe:: len(local_storage)

      Return the number of items in :object:`local_storage`.

   .. describe:: local_storage[key]

      Return the item of :object:`local_storage` with key *key*.  Raises a :exc:`KeyError` if *key* is
      not in :object:`local_storage`. Raises a :exc:`TypeError` if *key* is not a string.

   .. describe:: local_storage[key] = value

      Set ``local_storage[key]`` to *value*. The *value* must be a json compatible object.

   .. describe:: del local_storage[key]

      Remove ``local_storage[key]`` from :object:`local_storage`. :exc:`KeyError` raised is NOT raised if the key is not in :object:`local_storage`.

   .. describe:: key in local_storage

      Return ``True`` if :object:`local_storage` has a key *key*, else ``False``.

   .. describe:: iter(local_storage)

      Return an iterator over the keys of the dictionary.  This is a shortcut
      for ``iter(local_storage.keys())``.

   .. method:: clear()

      Remove all items from the dictionary.

   .. method:: get(key[, default])

      Return the value for *key* if *key* is in :object:`local_storage`, else *default*.
      If *default* is not given, it defaults to ``None``, so that this method
      never raises a :exc:`KeyError`.

   .. method:: items()

      Return a map iterator of :object:`local_storage`'s (``[key, value]`` pairs).

   .. method:: keys()

      Return a map iterator of the dictionary's keys.

   .. method:: pop(key[, default])

      If *key* is in :object:`local_storage`, remove it and return its value, else return
      *default*.  If *default* is not given, it defaults to ``None``, so that this method
      never raises a :exc:`KeyError`.

   .. method:: put(key, value)

      Equivalent to ``local_storage[key] = value``.

   .. method:: update([other])

      Update the :object:`local_storage` with the key/value pairs from *other*, overwriting
      existing keys.  Return ``None``.

      :meth:`update` accepts either a dictionary object or an iterable of
      key/value pairs (as tuples or other iterables of length two).  If keyword
      arguments are specified, :object:`local_storage` is then updated with those
      key/value pairs: ``d.update(red=1, blue=2)``.

   .. method:: values()

      Return a map iterator of :object:`local_storage`'s values.
