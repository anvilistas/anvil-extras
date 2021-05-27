# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import random

from . import style

__version__ = "1.2.0"

style_injector = style.Injector()


def get_uid(length=8):
    characters = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join([random.choice(characters) for _ in range(length)])
