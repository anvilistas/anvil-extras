# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil.js
from anvil.js import window as _window

__version__ = "1.6.0"
__all__ = ["local_storage", "indexed_db"]

_ForageModule = anvil.js.import_from("https://cdn.skypack.dev/localforage@1.10.0")

_forage = _ForageModule.default
_forage.dropInstance()


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
    _driver = None
    _stores = None

    def __new__(cls, store_name):
        if cls._driver is None:
            raise NotImplementedError(
                "StorageWrapper cannot be initiated without a valid _driver"
            )
        if not isinstance(store_name, str):
            raise TypeError(
                f"store_name should be a str, (got {store_name.__class__.__name__})"
            )
        known_stores = cls._stores
        if known_stores is None:
            # initialize the _stores cache
            known_stores = cls._stores = {}
        elif store_name in known_stores:
            return known_stores[store_name]

        store = object.__new__(cls)
        store._store = _forage.createInstance(
            {
                "storeName": store_name,
                "driver": [cls._driver, f"fail{cls._driver}"],
                "name": "anvil_extras",
            }
        )
        store._name = store_name
        known_stores[store_name] = store
        return store

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
        return f"<{self.__class__.__name__} for {self._name!r} store>"

    def __iter__(self):
        return self.keys()

    def __len__(self):
        return self._store.length()

    def keys(self):
        """returns the keys for the store as an iterator"""
        return self._store.keys()

    def items(self):
        """returns the items for the store as an iterator"""
        return (
            (key, _deserialize(self._store.getItem(key))) for key in self._store.keys()
        )

    def values(self):
        """returns the values for the store as an iterator"""
        return (_deserialize(self._store.getItem(key)) for key in self._store.keys())

    def store(self, key: str, value):
        """store a key value pair in the store"""
        self[key] = value

    put = store  # backward compatibility

    def get(self, key: str, default=None):
        """get a value from the store, returns the default value if the key is not in the store"""
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: str, default=None):
        """remove specified key and return the corresponding value.\n\nIf key is not found, default is returned"""
        try:
            return self.get(key, default)
        finally:
            del self[key]

    def clear(self):
        """clear all items from the store"""
        self._store.clear()

    def update(self, other, **kws):
        """update the store item with key/value pairs from other"""
        other = dict(other, **kws)
        for key, value in other.items():
            self[key] = value

    @classmethod
    def create_store(cls, store_name: str):
        """
        Create a new storage object inside the browser's IndexedDB or localStorage.
        e.g. todo_store = indexed_db.create_store('todos')
        message_store = indexed_db.create_store('messages')
        """
        return cls(store_name)


# The following defines a forage driver whose job is to
# try to access the appropriate browser store,
# catch the exception and the throw a nicer exception
def _fail_access(fn):
    def _do_fail(*args):
        # see what happens when we try to access the storage object
        msg = "Browser storage object is not available."
        try:
            fn()
        except Exception as e:
            msg += f"\nWhen trying to access the storage object got - {e}"
        raise RuntimeError(msg)

    return _do_fail


def _fail_db(*args):
    def check_db(res, rej):
        req = _window.indexedDB.open("anvil_extras")
        req.onerror = lambda e: rej(req.error.toString())
        req.onsuccess = lambda r: res(None)

    # this is asyncronous so use the Promise api
    anvil.js.await_promise(_window.Promise(check_db))


def _fail_ls(*args):
    _window.get("localStorage")


def _defineFailDriver(driver: str):
    fail_fn = _fail_db if driver == _forage.INDEXEDDB else _fail_ls
    fail_callback = _fail_access(fail_fn)
    _forage.defineDriver(
        {
            "_driver": f"fail{driver}",
            "_initStorage": lambda options: None,
            "clear": fail_callback,
            "getItem": fail_callback,
            "iterate": fail_callback,
            "key": fail_callback,
            "keys": fail_callback,
            "length": fail_callback,
            "removeItem": fail_callback,
            "setItem": fail_callback,
        }
    )


_defineFailDriver(_forage.INDEXEDDB)
_defineFailDriver(_forage.LOCALSTORAGE)


class IndexedDBWrapper(StorageWrapper):
    _driver = _forage.INDEXEDDB


indexed_db = IndexedDBWrapper.create_store("default")


class LocalStorageWrapper(StorageWrapper):
    _driver = _forage.LOCALSTORAGE


local_storage = LocalStorageWrapper.create_store("default")


def __getattr__(name):
    if name == "session_storage":
        raise Exception("deprecated - session_storage is no longer supported")
    raise AttributeError(name)


if __name__ == "__main__":
    for _ in local_storage, indexed_db:
        print(_)
        _["foo"] = "bar"
        print(_["foo"])
        del _["foo"]
        print(_.get("foo", "sentinel"))
        try:
            _["foo"]
        except KeyError as e:
            print(repr(e))
        _.put("foo", 1)
        print(_.pop("foo"))
        x = [{"a": "b"}, "foo"]
        _["x"] = x
        print(_["x"])
        print(_["x"] == x)
        print(_.get("x") == x)
        print(_.pop("x") == x)
        _["foo"] = None
        _["eggs"] = None
        _.update({"foo": "bar"}, eggs="spam", x=1)
        print(len(list(_.keys())) == 3, _["eggs"] == "spam")
        _.clear()
        print(len(list(_.keys())) == 0)
        print("==========")
