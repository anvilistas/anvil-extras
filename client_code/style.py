# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil.js.window import document

__version__ = "1.2.0"


class Injector:
    def __init__(self):
        self.injected = set()

    def inject(self, css):
        hashed = hash(css)
        if hashed not in self.injected:
            sheet = document.createElement("style")
            sheet.innerHTML = css
            document.body.appendChild(sheet)
            self.injected.add(hashed)
