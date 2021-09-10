# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "1.5.2"

from anvil import Label
from anvil import alert as anvil_alert

from . import _navigation


class AlertInfo:
    def __init__(self, active=False, dismissible=True, content=None):
        self.update(active, dismissible, content)

    def dismiss(self):
        if self.content is not None:
            self.content.raise_event("x-close-alert")

    def update(self, active, dismissible=True, content=None):
        self.active = active
        self.dismissible = dismissible
        self.content = content


current_alert = AlertInfo()

alert_btns = (("OK", True, "success"),)
confirm_btns = (("No", False, "danger"), ("Yes", True, "success"))
# defauult buttons in anvil included here for autocomplete
# and because providing any value overrides anvil's default buttons


def alert(
    content, title="", buttons=alert_btns, large=False, dismissible=True, role=None
):
    """use in the same way as anvil.alert
    If dismissible=True when a user navigates the alert will be closed
    If dismissible=False navigating will be prevented
    """
    if isinstance(content, str):
        content = Label(text=content)
    current_alert.update(True, dismissible, content)
    try:
        return anvil_alert(
            content,
            title=title,
            buttons=buttons,
            large=large,
            dismissible=dismissible,
            role=role,
        )
    finally:
        current_alert.update(False)


def confirm(
    content, title="", buttons=confirm_btns, large=False, dismissible=False, role=None
):
    return alert(content, title, buttons, large, dismissible, role)


def handle_alert_unload() -> bool:
    """
    if there is an active alert which is not dismissible then navigation is prevented
    return value indicates whether this function took control of the on_navigation
    """
    if not current_alert.active:
        return False
    elif current_alert.dismissible:
        current_alert.dismiss()
        return False
    else:
        _navigation.stopUnload()
        return True
