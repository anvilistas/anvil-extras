# MIT License
#
# Copyright (c) 2021 Owen Campbell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/meatballs/anvil-extras
from .. import session
from ._anvil_designer import MessagePillTemplate

__version__ = "0.1.5"

css = """
.anvil-role-message-pill {
    padding-left: 1em;
    border-radius: 2em;
}
"""
session.style_injector.inject(css)


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
