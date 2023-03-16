# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

__version__ = "2.2.2"


def enum(name, members):
    _ = type(name, (), {})()
    _.__dict__.update({member: member for member in members})
    return _


def join(iter, sep=" | "):
    return sep.join(map(repr, iter))
