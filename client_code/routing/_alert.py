# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "2.2.3"

from anvil.js.window import jQuery as _S


def handle_alert_unload() -> bool:
    """
    if there is an active alert which is not dismissible then navigation is prevented
    return value indicates whether this function took control of the on_navigation
    """
    current_alerts = _S(".modal")
    for alert_modal in current_alerts:
        alert_modal = _S(alert_modal)
        data = alert_modal.data("bs.modal")
        if data is None:
            continue
        elif not data.isShown:
            continue
        elif data.options and data.options.backdrop != "static":
            # bootstrap alerts have a backdrop of static when not dismissible
            alert_modal.modal("hide")
        else:
            from . import _navigation

            _navigation.stopUnload()
            return True
    return False
