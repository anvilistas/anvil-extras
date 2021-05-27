# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil_extras import ProgressBar, session

from ._anvil_designer import IndeterminateTemplate

__version__ = "1.2.0"

session.style_injector.inject(ProgressBar.css)


class Indeterminate(IndeterminateTemplate):
    def __init__(self, track_colour, indicator_colour, **properties):
        self.uid = session.get_uid()
        css = f"""
.anvil-role-indeterminate-progress-indicator-{self.uid} {{
  background-colour: {indicator_colour}
}}

.anvil-role-indeterminate-progress-indicator-{self.uid}:before {{
  background-color: {track_colour}

}}
"""
        session.style_injector.inject(css)
        self.role = "progress-track"
        self.indicator_panel.role = [
            "indeterminate-progress-indicator",
            f"indeterminate-progress-indicator-{self.uid}",
        ]
        self.indicator_panel.background = indicator_colour
        self.init_components(**properties)
