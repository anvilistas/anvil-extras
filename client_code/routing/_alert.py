# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "1.5.2"

from anvil import Label
from anvil import alert as anvil_alert
from anvil import confirm as anvil_confirm

from . import _navigation


class AlertInfo:
    def __init__(self, active=False, dismissible=True, content=None):
        self.update(active, dismissible, content)

    def dismiss(self) -> bool:
        """returns a bool as to whether the alert was dismissed"""
        if not self.active:
            return True  # nothing to dismiss
        if self.dismissible and self.content is not None:
            self.content.raise_event("x-close-alert")
            return True
        return False

    def update(self, active, dismissible=True, content=None):
        self.active = active
        self.dismissible = dismissible
        self.content = content


current_alert = AlertInfo()
no_arg = object()
# we use sentinel since the presence of an arg determines the behaviour of an alert
alert_kws = ("title", "buttons", "large", "role")


def wrap_alert(content, dismissible, is_confirm=False, **kws):
    if isinstance(content, str):
        content = Label(text=content)
    current_alert.update(True, dismissible, content)
    for key in alert_kws:
        if kws.get(key) is no_arg:
            del kws[key]
            # remove sentinel values
    try:
        if is_confirm:
            return anvil_confirm(content, dismissible=dismissible, **kws)
        else:
            return anvil_alert(content, dismissible=dismissible, **kws)
    finally:
        current_alert.update(False)


# we keep the same order as defined in the api docs
# use kws for future proofing additional anvil args
def alert(
    content,
    *,
    title=no_arg,
    buttons=no_arg,
    large=no_arg,
    dismissible=True,
    role=no_arg,
    **kws
):
    """use in the same way as anvil.alert
    If dismissible=True when a user navigates the alert will be closed
    If dismissible=False navigating will be prevented
    """
    return wrap_alert(
        content,
        dismissible,
        title=title,
        buttons=buttons,
        large=large,
        role=role,
        **kws
    )


def confirm(
    content,
    *,
    title=no_arg,
    buttons=no_arg,
    large=no_arg,
    dismissible=False,
    role=no_arg,
    **kws
):
    return wrap_alert(
        content,
        dismissible,
        is_confirm=True,
        title=title,
        buttons=buttons,
        large=large,
        role=role,
        **kws
    )


def handle_alert_unload() -> bool:
    """
    if there is an active alert which is not dismissible then navigation is prevented
    return value indicates whether this function took control of the on_navigation
    """
    if current_alert.dismiss():
        return False
    _navigation.stopUnload()
    return True
