# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras


from functools import cache

__version__ = "1.3.1"

_dict_setitem = dict.__setitem__


class BindingRefreshDict(dict):
    """A dict that calls refresh_data_bindings when its content changes"""

    def _refresh_data_bindings(self):
        forms = getattr(self, "_forms", [])
        for form in forms:
            form.refresh_data_bindings()

    def __setitem__(self, key, value):
        _dict_setitem(self, key, value)
        self._refresh_data_bindings()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._refresh_data_bindings()


def _item_override(cls):
    """Generate a property to override a form's 'item' attribute"""
    base_item = super(cls, cls).item

    def item_getter(self):
        return base_item.__get__(self, cls)

    def item_setter(self, item):
        item = (
            item if isinstance(item, BindingRefreshDict) else BindingRefreshDict(item)
        )
        # use a set here so that subforms using the same item can also trigger
        # refresh_data_bindings
        forms = item._forms = getattr(item, "_forms", set())
        forms.add(self)
        base_item.__set__(self, item)

    return property(item_getter, item_setter)


@cache
def auto_refreshing(cls):
    """A decorator for a form class to refresh data bindings automatically"""
    cls.item = _item_override(cls)
    return cls
