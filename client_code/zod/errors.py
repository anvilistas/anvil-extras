# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

default_error_map = None
error_map = None

__version__ = "2.2.2"


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
