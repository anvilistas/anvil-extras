# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "3.1.0"

import anvil
from anvil import alert as anvil_alert

active_alerts = []


def handle_alert_unload() -> bool:
    for alert in reversed(active_alerts):
        if alert.blocking:
            from . import _navigation

            _navigation.stopUnload()
            return True
        else:
            alert.content.raise_event("x-close-alert")

    return False


class ActiveAlert:
    def __init__(self, content, blocking):
        self.content = content
        self.blocking = blocking

    def __enter__(self):
        active_alerts.append(self)

    def __exit__(self, *args):
        global active_alerts
        active_alerts = [x for x in active_alerts if x is not self]


def alert(content, *args, dismissible=True, **kws):
    if type(content) is str:
        content = anvil.Label(text=content)

    with ActiveAlert(content, blocking=not dismissible):
        return anvil_alert(content, *args, dismissible=dismissible, **kws)
