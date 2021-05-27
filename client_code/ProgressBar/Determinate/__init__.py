# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil.js.window import document

from anvil_extras import ProgressBar, session

from ._anvil_designer import DeterminateTemplate

__version__ = "1.2.0"

session.style_injector.inject(ProgressBar.css)


class Determinate(DeterminateTemplate):
    def __init__(self, track_colour, indicator_colour, **properties):
        self.uid = session.get_uid()
        css = f"""
:root {{
  --progress-{self.uid}: 50%;
}}

.anvil-role-progress-indicator-{self.uid} {{
  width: var(--progress-{self.uid});
}}
        """
        session.style_injector.inject(css)
        self.role = "progress-track"
        self.indicator_panel.role = [
            "progress-indicator",
            f"progress-indicator-{self.uid}",
        ]
        self.background = track_colour
        self.indicator_panel.background = indicator_colour
        self.init_components(**properties)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        document.body.style.setProperty(f"--progress-{self.uid}", f"{value:%}")
