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
from anvil.js.window import document
from extras import ProgressBars, session

from ._anvil_designer import ProgressBarTemplate

__version__ = "0.1.5"
session.style_injector.inject(ProgressBars.css)


class ProgressBar(ProgressBarTemplate):
    def __init__(self, **properties):
        self.uid = session.get_uid()
        css = f"""
:root {{
  --track-colour-{self.uid}: #b3d4fc;
  --indicator-colour-{self.uid}: #1976D2;
  --progress-{self.uid}: 50%;
}}

.anvil-role-progress-track-{self.uid} {{
  background-color: var(--track-colour-{self.uid});
  width: 100%;
}}

.anvil-role-progress-indicator-{self.uid} {{
  background-color: var(--indicator-colour-{self.uid});
  width: var(--progress-{self.uid});
}}
        """
        session.style_injector.inject(css)
        self.role = ["progress-track", f"progress-track-{self.uid}"]
        self.indicator_panel.role = ["progress-indicator", f"progress-indicator-{self.uid}"]
        self.init_components(**properties)

    @property
    def track_colour(self):
        return self._track_colour

    @track_colour.setter
    def track_colour(self, value):
        self._track_colour = value
        document.body.style.setProperty(f"--track-colour-{self.uid}", value)

    @property
    def indicator_colour(self):
        return self._indicator_colour

    @indicator_colour.setter
    def indicator_colour(self, value):
        self._indicator_colour = value
        document.body.style.setProperty(f"--indicator-colour-{self.uid}", value)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        document.body.style.setProperty(f"--progress-{self.uid}", f"{value:%}")