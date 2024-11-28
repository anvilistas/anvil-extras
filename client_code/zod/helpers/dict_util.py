# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "3.1.0"


def merge_shapes(a, b):
    return {**a, **b}


def getitem(mapping, item, default):
    try:
        return mapping[item]
    except LookupError:
        return default


class DictLike:
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def keys(self):
        return self.__dict__.keys()

    def __contains__(self, key):
        return key in self.__dict__

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __repr__(self):
        items = self.__dict__.items()
        return f"{type(self).__name__}({', '.join(f'{k}={v!r}' for k, v in items)})"

    def __str__(self):
        return str(self.__dict__)
