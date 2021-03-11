# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
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
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil_extras import ProgressBar, session

from ._anvil_designer import IndeterminateTemplate

__version__ = "1.0.0"

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
