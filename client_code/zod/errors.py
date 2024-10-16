# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

default_error_map = None
error_map = None

__version__ = "3.0.0"


def get_default_error_map():
    global default_error_map
    if default_error_map is None:
        from .locales.en import error_map

        default_error_map = error_map
    return default_error_map


def get_error_map():
    global error_map
    if default_error_map is None:
        get_default_error_map()
    return error_map or default_error_map


def set_error_map(map):
    global error_map
    error_map = map
