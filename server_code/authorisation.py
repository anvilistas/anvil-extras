# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import functools

import anvil.users
from anvil.tables import app_tables

__version__ = "2.6.1"

config = {"get_roles_row": None}


def set_config(**kwargs):
    if "get_roles_row" in kwargs:
        set_user_roles_getter(kwargs["get_roles_row"])


def set_user_roles_getter(option):
    user = anvil.users.get_user()
    if option is None:
        config["get_roles_row"] = app_tables.users.get(user=user)['roles']
    elif callable(option):  # row object
        config["get_roles_row"] = option['roles']
    elif isinstance(option, str):  # table name
        config["get_roles_row"] = getattr(app_tables, option).get(user=user)['roles']
        print(config["get_roles_row"])
    else:
        raise TypeError("set_user_roles_getter: option is not valid.")


def authentication_required(func):
    """A decorator to ensure only a valid user can call a server function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if anvil.users.get_user() is None:
            raise ValueError("Authentication required")
        else:
            return func(*args, **kwargs)

    return wrapper


def has_permission(permissions):
    """Returns True/False depending on whether a user has permission or not"""
    user = anvil.users.get_user()
    if user is None:
        return False

    if isinstance(permissions, str):
        required_permissions = set([permissions])
    else:
        required_permissions = set(permissions)

    try:
        user_permissions = set(
            permission["name"]
            for role in config["get_roles_row"]
            for permission in role["permissions"]
        )
    except TypeError:
        return False

    return required_permissions.issubset(user_permissions)


def check_permissions(permissions):
    """Checks a users permissions, raises ValueError if user does not have permissions"""
    if has_permission(permissions):
        return

    user = anvil.users.get_user()
    fail = "Authentication" if user is None else "Authorisation"

    raise ValueError(f"{fail} required")


def authorisation_required(permissions):
    """A decorator to ensure a user has sufficient permissions to call a server function"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            check_permissions(permissions)
            return func(*args, **kwargs)

        return wrapper

    return decorator
