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


def _validate_mode(mode):
    if mode not in ("classic", "usermap"):
        raise ValueError("The authorisation mode can only be 'classic' or 'usermap'")


def set_mode(mode):
    global _default_mode
    _validate_mode(mode)
    _default_mode = mode

def set_config(**kwargs):
    if "get_roles_row" in kwargs:
        set_user_roles_getter(kwargs["get_roles_row"])


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

    if _default_mode == "classic":
        user_permissions = has_permission_classic(user)
    else:
        user_permissions = has_permission_usermap(user)

    return required_permissions.issubset(user_permissions)


def has_permission_classic(user):
    """Returns user_permissions set for classic mode."""
    try:
        user_permissions = set(
            permission["name"]
            for role in user["roles"]
            for permission in role["permissions"]
        )
    except TypeError:
        return False
    return user_permissions


def has_permission_usermap(user):
    """Returns user_permissions set for usermap mode."""
    usermap = app_tables.usermap.get(user=user)
    try:
        user_permissions = set(
            permission["name"]
            for role in usermap["roles"]
            for permission in role["permissions"]
        )
    except TypeError:
        return False
    return user_permissions


def check_permissions(permissions):
    """Checks a users permissions, raises ValueError if user does not have permissions"""
    if has_permission(permissions):
        return

    user = anvil.users.get_user()
    fail = "Authentication" if user is None else "Authorisation"

    raise ValueError(f"{fail} required")





def set_user_roles_getter(option):
    if option is None:
        config["get_roles_row"] = None
    elif callable(option):
        config["get_roles_row"] = option
    elif isinstance(option, str):
        config["get_roles_row"] = lambda user: getattr(app_tables, option).get(
            user=user
        )
    elif ...:  # option is app_table
        config["get_roles_row"] = lambda user: option.get(user=user)
    else:
        raise TypeError(...)


def authorisation_required(permissions):
    """A decorator to ensure a user has sufficient permissions to call a server function"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            check_permissions(permissions)
            return func(*args, **kwargs)

        return wrapper

    return decorator
