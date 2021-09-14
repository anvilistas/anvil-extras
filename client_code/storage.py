# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js import window as _window

from utils._component_helpers import _add_script

__version__ = "1.5.2"
__all__ = ["local_storage", "indexed_db"]


_Proxy = type(_window)
_Object = _window.Object


def _deserialize(obj):
    """convert simple proxy objects (and nested simple proxy objects) to dictionaries"""
    # @TODO datetime objects - we'd also need a _serialize method for that
    if isinstance(obj, list):
        ret = []
        for item in obj:
            ret.append(_deserialize(item))
        return ret
    elif type(obj) is _Proxy and obj.__class__ == _Object:
        # Then we're a simple proxy object
        # keys are strings so only _deserialize the values
        ret = {}
        # use _Object.keys to avoid possible name conflict
        for key in _Object.keys(obj):
            ret[key] = _deserialize(obj[key])
        return ret
    else:
        # we're either bytes, str, ints, floats, None, bool
        return obj


class StorageWrapper:
    def __init__(self, store, driver, name):
        self._store = store
        self._driver = driver
        self._name = name

    def is_available(self):
        """check if the store object is available and accessible."""
        # in some browsers localStorageWrapper might not be available
        if not self._store.supports(self._driver):
            # we cn't rely on this method - it's just for browser support
            return False
        try:
            self._store.length()
            # call a method in the store to activate the store
            return True
        except Exception:
            return False

    def __getitem__(self, key):
        if key in self._store.keys():
            return _deserialize(self._store.getItem(key))
        raise KeyError(key)

    def __setitem__(self, key, val):
        self._store.setItem(key, val)

    def __delitem__(self, key):
        # we can't block here so do a Promise hack
        _window.Promise(lambda res, rej: self._store.removeItem(key))
        return None

    def __contains__(self, key):
        return key in self._store.keys()

    def __repr__(self):
        # we can't print the items like a dictionary since we get a SuspensionError here
        return f"<{driver_names[self._driver]} for {self._name!r} store>"

    def __iter__(self):
        return self.keys()

    def __len__(self):
        return self._store.length()

    def keys(self):
        """returns the keys for local storage as an iterator"""
        return self._store.keys()

    def items(self):
        """returns the items for local storage as an iterator"""
        return (
            (key, _deserialize(self._store.getItem(key))) for key in self._store.keys()
        )

    def values(self):
        """returns the values for local storage as an iterator"""
        return (_deserialize(self._store.getItem(key)) for key in self._store.keys())

    def store(self, key, value):
        """put a key value pair into local storage"""
        self[key] = value

    put = store  # backward compatibility

    def get(self, key, default=None):
        """get a value from local storage, returns the default value if the key is not in local storage"""
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key, default=None):
        """remove specified key and return the corresponding value.\n\nIf key is not found, default is returned"""
        try:
            return self.get(key, default)
        finally:
            del self[key]

    def clear(self):
        """clear all items from local storage"""
        self._store.clear()

    def update(self, other, **kws):
        """update the local storage item with key/value pairs from other"""
        other = dict(other, **kws)
        for key, value in other.items():
            self[key] = value

    def __eq__(self, other):
        if not isinstance(other, StorageWrapper):
            return NotImplemented
        return self._driver == other._driver and self._name == other._name

    def get_store(self, name):
        """
        Create a new storage object. Inside either local_storage or indexed_db.
        e.g. todo_store = indexed_db.get_store('todos')
        message_store = indexed_db.get_store('messages')
        """
        return StorageWrapper(
            self._store.createInstance(
                {"storeName": name, "driver": self._driver, "name": "anvil_extras"}
            ),
            self._driver,
            name,
        )


_add_script(
    """
<script src="https://cdn.jsdelivr.net/npm/localforage@1.10.0/dist/localforage.min.js"></script>
"""
)

_forage = _window.localforage
_forage.dropInstance()


def _failed(*args):
    # see what happens when we try to access the storage object
    msg = "browser storage object is not available - see documentation."
    try:
        _window.get("localStorage")

        def check_db(res, rej):
            req = _window.get("indexedDB").open("anvil_extras")
            req.onerror = lambda e: rej(req.error.toString())
            req.onsuccess = lambda r: res(None)

        _window.Function("callback", "return new Promise(callback)")(check_db)
    except Exception as e:
        msg += f"\nWhen trying to access the storage object got - {e}"
    raise RuntimeError(msg)


_forage.defineDriver(
    {
        "_driver": "failDriver",
        "_initStorage": lambda options: None,
        "clear": _failed,
        "getItem": _failed,
        "iterate": _failed,
        "key": _failed,
        "keys": _failed,
        "length": _failed,
        "removeItem": _failed,
        "setItem": _failed,
    }
)

_indexed_db_wrapper = _forage.createInstance(
    {
        "name": "anvil_extras",
        "storeName": "default",
        "driver": [_forage.INDEXEDDB, "failDriver"],
    }
)
indexed_db = StorageWrapper(_indexed_db_wrapper, _forage.INDEXEDDB, "default")

_local_store_wrapper = _forage.createInstance(
    {
        "name": "anvil_extras",
        "storeName": "default",
        "driver": [_forage.LOCALSTORAGE, "failDriver"],
    }
)
local_storage = StorageWrapper(_local_store_wrapper, _forage.LOCALSTORAGE, "default")

driver_names = {
    _forage.INDEXEDDB: "IndexedDBWrapper",
    _forage.LOCALSTORAGE: "LocalStorageWrapper",
}


def __getattr__(name):
    if name == "session_storage":
        raise Exception("deprecated - session_storage is no longer supported")
    raise AttributeError(name)


if __name__ == "__main__":
    for db in local_storage, indexed_db:
        print(db)
        db["foo"] = "bar"
        print(db["foo"])
        del db["foo"]
        print(db.get("foo", "sentinel"))
        try:
            db["foo"]
        except KeyError as e:
            print(repr(e))
        db.put("foo", 1)
        print(db.pop("foo"))
        x = [{"a": "b"}, "foo"]
        db["x"] = x
        print(db["x"])
        print(db["x"] == x)
        print(db.get("x") == x)
        print(db.pop("x") == x)
        db["foo"] = None
        db["eggs"] = None
        db.update({"foo": "bar"}, eggs="spam", x=1)
        print(len(list(db.keys())) == 3, db["eggs"] == "spam")
        db.clear()
        print(len(list(db.keys())) == 0)
        print("==========")
