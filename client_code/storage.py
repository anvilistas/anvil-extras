# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import json as _json

from anvil import app
from anvil.js import window as _window

__version__ = "1.5.2"
__all__ = ["local_storage", "session_storage"]

_prefix = "anvil_storage_"
_prefix_len = len(_prefix)


class Storage:
    def __init__(self, store):
        self._store = store

    def _check_store(self):
        # in some browsers localStorage might not be available
        # we don't throw the error until we try to access the store
        if self._store is None:
            raise RuntimeError("browser storage is not available")

    def _mangle_key(self, key):
        # we mangle the names so that we avoid conflicts
        self._check_store()
        if not isinstance(key, str):
            raise TypeError("storage keys must be strings")
        return key if key.startswith(_prefix) else _prefix + key

    def _filter_store(self):
        return filter(lambda key: key.startswith(_prefix), self._store.keys())

    def _map_store(self, predicate):
        self._check_store()
        return map(predicate, self._filter_store())

    def __getitem__(self, key):
        ret = self._store.getItem(self._mangle_key(key))
        if ret is None:
            raise KeyError(key)
        return _json.loads(ret)

    def __setitem__(self, key, val):
        key = self._mangle_key(key)
        try:
            val = _json.dumps(val)
        except Exception as e:
            raise type(e)(f"There was a problem converting the value into json: {e}")
        self._store.setItem(key, val)

    def __delitem__(self, key):
        self._store.removeItem(self._mangle_key(key))

    def __contains__(self, key):
        return self._mangle_key(key) in self._store

    def __repr__(self):
        pairs = ", ".join(f"{key!r}: {val!r}" for key, val in self.items())
        return f"Storage({{{pairs}}})"

    def __iter__(self):
        return self.keys()

    def keys(self):
        """returns the keys for local storage as an iterator"""
        return self._map_store(lambda key: key[_prefix_len:])

    def items(self):
        """returns the items for local storage as an iterator"""
        return self._map_store(lambda key: (key[_prefix_len:], self.__getitem__(key)))

    def values(self):
        """returns the values for local storage as an iterator"""
        return self._map_store(lambda key: self.__getitem__(key))

    def put(self, key, value):
        """put a key value pair into local storage"""
        self[key] = value

    def get(self, key, default=None):
        """get a value from local storage, returns the default value if the key is not in local storage"""
        try:
            return self.__getitem__(key)
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
        for key in self._filter_store():
            self._store.removeItem(key)

    def update(self, other, **kws):
        """update the local storage item with key/value pairs from other"""
        other = dict(other, **kws)
        for key, value in other.items():
            self[key] = value


try:
    local_storage = Storage(_window.get("localStorage"))
    session_storage = Storage(_window.get("sessionStorage"))
except Exception as err:
    if repr(err).startswith("External") and "debug" in app.environment["tags"]:
        print(
            "Warning: Access to storage denied, likely due to browser permissions. "
            "Dictionary alternatives, which will not persist between browser "
            "sessions, are being substituted for 'local_storage' and "
            "'session_storage'. The following error will be raised if this occurs "
            "outside Anvil's 'debug' mode:"
        )
        print(repr(RuntimeError(err)))
        local_storage = {}
        session_storage = {}
    else:
        raise (RuntimeError(err))


if __name__ == "__main__":
    print(local_storage)
    for k, v in local_storage.items():
        print(k, v)
    local_storage["foo"] = "bar"
    print(local_storage["foo"])
    del local_storage["foo"]
    print(local_storage.get("foo"))
    try:
        local_storage["foo"]
    except KeyError as e:
        print(repr(e))
    local_storage.put("foo", 1)
    print(local_storage.pop("foo"))
    x = {"abc": 123}
    local_storage["x"] = x
    print("x" in local_storage)
    print(local_storage["x"] == x)
    print(local_storage.get("x") == x)
    print(local_storage.pop("x") == x)
    local_storage["foo"] = None
    local_storage["eggs"] = None
    local_storage.update({"foo": "bar"}, eggs="spam", x=1)
    print(len(list(local_storage.keys())) == 3, local_storage["eggs"] == "spam")
    local_storage.clear()
    print(len(list(local_storage.keys())) == 0)
