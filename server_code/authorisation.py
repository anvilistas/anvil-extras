# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import functools
from operator import itemgetter

import anvil.users
from anvil.tables import app_tables

__version__ = "3.6.1"

config = {"get_roles": itemgetter("roles")}

sentinel = object()


def set_config(**kwargs):
    if "get_roles" in kwargs:
        _set_user_roles_getter(kwargs["get_roles"])


def _get_roles_from_table(table_name, user):
    return getattr(app_tables, table_name).get(user=user)["roles"]


def _set_user_roles_getter(option):
    if option is None:
        config["get_roles"] = itemgetter("roles")
    elif isinstance(option, str):  # table name
        config["get_roles"] = functools.partial(_get_roles_from_table, option)
    else:
        raise TypeError("get_roles: option is not valid.")


def authentication_required(func):
    """A decorator to ensure only a valid user can call a server function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if anvil.users.get_user() is None:
            raise ValueError("Authentication required")
        else:
            return func(*args, **kwargs)

    return wrapper


def has_permission(permissions, user=sentinel):
    """Returns True/False depending on whether a user has permission or not"""
    user = anvil.users.get_user() if user is sentinel else user

    if user is None:
        return False

    if isinstance(permissions, str):
        required_permissions = set([permissions])
    else:
        required_permissions = set(permissions)

    try:
        user_permissions = set(
            permission["name"]
            for role in config["get_roles"](user)
            for permission in role["permissions"]
        )
    except TypeError:
        return False

    return required_permissions.issubset(user_permissions)


def check_permissions(permissions, user=sentinel):
    """Checks a users permissions, raises ValueError if user does not have permissions"""
    user = anvil.users.get_user() if user is sentinel else None

    if has_permission(permissions, user=user):
        return

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
