# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from ..utils._component_helpers import _html_injector
from ._anvil_designer import MessagePillTemplate

__version__ = "2.2.3"

css = """
.anvil-role-message-pill {
    padding-left: 1em;
    border-radius: 2em;
}
"""
_html_injector.css(css)


class MessagePill(MessagePillTemplate):
    backgrounds = dict(
        info="#bde5f8", success="#dff2bf", warning="#feefb3", error="#ffd2d2"
    )
    foregrounds = dict(
        info="#00529b", success="#4f8a10", warning="#9f6000", error="#d8000c"
    )
    icons = dict(
        info="fa:info-circle",
        success="fa:check",
        warning="fa:warning",
        error="fa:times-circle",
    )

    def __init__(self, **properties):
        self.label.role = "message-pill"
        self.init_components(**properties)

    @property
    def level(self):
        return self.item["level"]

    @level.setter
    def level(self, value):
        if value not in ("info", "success", "warning", "error"):
            raise ValueError(
                "level must be one of 'info', 'success', 'warning' or 'error'"
            )
        self.item["level"] = value
        self.label.background = self.backgrounds[value]
        self.label.foreground = self.foregrounds[value]
        self.label.icon = self.icons[value]

    @property
    def message(self):
        return self.item["message"]

    @message.setter
    def message(self, value):
        self.item["message"] = value
        self.label.text = value
