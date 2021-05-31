# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import random

from anvil.js import get_dom_node

from . import style

__version__ = "1.3.0"
characters = "abcdefghijklmnopqrstuvwxyz0123456789"

style_injector = style.Injector()


def get_dom_node_id(component):
    node = get_dom_node(component)
    if not node.id:
        node.id = "".join([random.choice(characters) for _ in range(8)])
    return node.id
