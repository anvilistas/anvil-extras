# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras


from functools import lru_cache

from anvil.server import portable_class

__version__ = "2.2.3"


def wrap_method(meth_name, refresh=False):
    def wrapped(self, *args, **kws):
        rv = getattr(self._obj, meth_name)(*args, **kws)
        if refresh:
            self._refresh_data_bindings()
        return rv

    wrapped.__name__ = meth_name
    wrapped.__qualname__ = "ProxyItem." + meth_name
    return wrapped


@portable_class
class ProxyItem:
    """A proxy that calls refresh_data_bindings when the underlying item changes"""

    __slots__ = {"_obj", "_forms"}

    def __init__(self, obj):
        self._obj = obj

    def _refresh_data_bindings(self):
        forms = getattr(self, "_forms", [])
        for form in forms:
            form.refresh_data_bindings()

    __getitem__ = wrap_method("__getitem__")
    __setitem__ = wrap_method("__setitem__", True)
    __delitem__ = wrap_method("__delitem__", True)
    get = wrap_method("get")
    update = wrap_method("update", True)
    pop = wrap_method("pop", True)
    clear = wrap_method("clear", True)
    keys = wrap_method("keys")
    values = wrap_method("values")
    items = wrap_method("items")

    def __bool__(self):
        return bool(self._obj)

    def __eq__(self, other):
        return self._obj == other

    def __iter__(self):
        return iter(self._obj)

    def __contains__(self, other):
        return other in self._obj

    def __len__(self):
        return len(self._obj)

    def __hash__(self):
        return hash(self._obj)

    def __setattr__(self, attr: str, val) -> None:
        if attr in self.__slots__:
            return object.__setattr__(self, attr, val)
        rv = setattr(self._obj, attr, val)
        self._refresh_data_bindings()
        return rv

    def __getattr__(self, attr):
        return getattr(self._obj, attr)

    def __repr__(self):
        return f"proxy_item({self._obj!r})"

    def __serialize__(self, info):
        return self._obj

    @staticmethod
    def __new_deserialized__(obj, info):
        return obj


# Backwards Compatability
BindingRefreshDict = ProxyItem


def _mk_init_components(cls):
    """Generate a method to override a form's 'init_components' method"""
    super_init = super(cls, cls).init_components

    def init_components(self, item=None, **props):
        if item is not None:
            return super_init(self, item=item, **props)
        elif self.item == {}:
            return super_init(self, item={}, **props)
        else:
            # don't provide the item if we've already set one
            return super_init(self, **props)

    return init_components


def _item_override(cls):
    """Generate a property to override a form's 'item' attribute"""
    base_item = super(cls, cls).item

    def item_getter(self):
        return base_item.__get__(self, cls)

    def item_setter(self, item):
        item = item if isinstance(item, ProxyItem) else ProxyItem(item)
        # use a set here so that subforms using the same item can also trigger
        # refresh_data_bindings
        forms = item._forms = getattr(item, "_forms", set())
        forms.add(self)
        base_item.__set__(self, item)

    return property(item_getter, item_setter)


@lru_cache(maxsize=None)
def auto_refreshing(cls):
    """A decorator for a form class to refresh data bindings automatically"""
    cls.item = _item_override(cls)
    cls.init_components = _mk_init_components(cls)
    return cls
