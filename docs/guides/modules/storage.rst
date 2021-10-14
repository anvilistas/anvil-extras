Storage
=======

Introduction
------------
Browsers have various mechanisms to store data. ``localStorage`` and ``IndexedDB`` are two such mechanisms. These are particularly useful for storing data offline.

The anvil_extras :mod:`storage` module provides wrappers around both these storage mechanisms in a convenient dictionary like API.

In order to store data you'll need a store object. You can import the default store objects :attr:`local_storage` or :attr:`indexed_db`.
Alternatively create your own store object using the classmethod ``create_store(store_name)``.

*NB: when working in the IDE the app is running in an IFrame and the storage objects may not be available. This can be fixed by changing your browser settings.
Turning the shields down in Brave or making sure not to block third party cookies in Chrome should fix this.*


Which to chose?
+++++++++++++++
| If you have small amounts of data which can be converted to JSON - use :attr:`local_storage`.
| If you have more data which can be converted to JSON (also ``bytes``) - use :attr:`indexed_db`.

``datetime`` and ``date`` objects are also supported.
If you want to store anything else you'll need to convert it to something JSONable first.


Usage Examples
--------------

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


Create an offline todo app
++++++++++++++++++++++++++

.. code-block:: python

    from anvil_extras.storage import indexed_db
    from anvil_extras.uuid import uuid4

    todo_store = indexed_db.create_store('todos')
    # create_store() is a classmethod that takes a store_name
    # it will create another store object inside the browsers IndexedDB
    # or return the store object if it already exists
    # the todo_store acts as dictionary like object

    class TodoPage(TodoPageTemplate):
        def __init__(self, **properties):
            self.init_components(**properties)
            self.todo_panel.items = list(todo_store.values())

        def save_todo_btn_click(self, **event_args):
            if not self.todo_input.text:
                return
            id = str(uuid4())
            todo = {"id": id, "todo": self.todo_input.text, "completed": False}
            todo_store[id] = todo
            self.todo_panel.items = self.todo_panel.items + [todo]
            self.todo_input.text = ""



API
---

.. class:: StorageWrapper()
           IndexedDBWrapper()
           LocalStorageWrapper()

    both :attr:`indexed_db` and :attr:`local_storage` are instances of the dictionary like classes :class:`IndexedDBWrapper` and :class:`LocalStorageWrapper` respectively.

    .. classmethod:: create_store(name)

        Create a store object. e.g. ``todo_store = indexed_db.create_store('todos')``. This will create a new store inside the browser's ``IndexedDB`` and return an :class:`IndexedDBWrapper` instance.
        The :attr:`indexed_db` object is equivalent to ``indexed_db.create_store('default')``. To explore this further, open up devtools and find ``IndexedDB`` in the Application tab.
        Since :attr:`create_store` is a classmethod you can also do ``todo_store = IndexedDBWrapper.create_store('todos')``.

    .. describe:: is_available()

        Check if the storage object is supported. Returns a ``boolean``.


    .. describe:: list(store)

        Return a list of all the keys used in the *store*.

    .. describe:: len(store)

        Return the number of items in *store*.

    .. describe:: store[key]

        Return the value of *store* with key *key*.  Raises a :exc:`KeyError` if *key* is
        not in *store*.

    .. describe:: store[key] = value

        Set ``store[key]`` to *value*. If the value is not a JSONable data type it may be stored incorrectly.
        If storing ``bytes`` objects it is best to use the :attr:`indexed_db` store.
        ``datetime`` and ``date`` objects are also supported.

    .. describe:: del store[key]

        Remove ``store[key]`` from *store*.

    .. describe:: key in store

        Return ``True`` if *store* has a key *key*, else ``False``.

    .. describe:: iter(store)

        Return an iterator over the keys of the *store*.  This is a shortcut
        for ``iter(store.keys())``.

    .. method:: clear()

        Remove all items from the *store*.

    .. method:: get(key[, default])

        Return the value for *key* if *key* is in *store*, else *default*.
        If *default* is not given, it defaults to ``None``, so that this method
        never raises a :exc:`KeyError`.

    .. method:: items()

        Return an iterator of the *store*'s ``(key, value)`` pairs.

    .. method:: keys()

        Return an iterator of the *store*'s keys.

    .. method:: pop(key[, default])

        If *key* is in *store*, remove it and return its value, else return
        *default*.  If *default* is not given, it defaults to ``None``, so that this method
        never raises a :exc:`KeyError`.

    .. method:: store(key, value)

        Equivalent to ``store[key] = value``.

    .. method:: update([other])

        Update the *store* with the key/value pairs from *other*, overwriting
        existing keys.  Return ``None``.

        :meth:`update` accepts either a dictionary object or an iterable of
        key/value pairs (as tuples or other iterables of length two).  If keyword
        arguments are specified, *store* is then updated with those
        key/value pairs: ``store.update(red=1, blue=2)``.

    .. method:: values()

        Return an iterator of the *store*'s values.
