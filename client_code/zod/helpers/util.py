# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "2.6.2"


def enum(name, members):
    _ = type(name, (), {})()
    _.__dict__.update({member: member for member in members})
    return _


def join(iter, sep=" | "):
    return sep.join(map(repr, iter))
