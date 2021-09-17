# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "1.6.0"

from anvil.js.window import jQuery as _S

from . import _navigation

alert_modal = _S("#alert-modal")


def handle_alert_unload() -> bool:
    """
    if there is an active alert which is not dismissible then navigation is prevented
    return value indicates whether this function took control of the on_navigation
    """
    data = alert_modal.data("bs.modal")
    if data is None:
        return False
    elif not data.isShown:
        return False
    elif data.options and data.options.backdrop != "static":
        # bootstrap alerts have a backdrom of static when not dismissible
        alert_modal.modal("hide")
        return False
    _navigation.stopUnload()
    return True
