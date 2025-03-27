# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import anvil.js

from anvil_extras.utils._component_helpers import _css_length, _get_color, set_hook

__version__ = "3.1.0"

css = """ .ae-progress-bar {
    display: block;
    margin: 0;
    --ae-bar-height: 3px;
    --ae-track-color: #b3d4fc;
    --ae-indicator-color: #1976D2;
    --ae-progress: 0;
    width: 100%;
    height: var(--ae-bar-height);
}

.ae-progress-indicator {
    height: 100%;
}

.ae-progress-bar.ae-determinate {
    background-color: var(--ae-track-color);
}

.ae-progress-bar.ae-indeterminate {
    background-color: var(--ae-indicator-color);
}

.ae-determinate .ae-progress-indicator {
    width: var(--ae-progress);
    background-color: var(--ae-indicator-color);
}

.ae-indeterminate .ae-progress-indicator, .ae-indeterminate .ae-progress-indicator:before {
  width: 100%;
  margin: 0;
}

.ae-indeterminate .ae-progress-indicator {
  display: flex;
}

.ae-indeterminate .ae-progress-indicator:before {
  content: '';
  -webkit-animation: ae-running-progress 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  animation: ae-running-progress 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  background-color: var(--ae-track-color);
}

@-webkit-keyframes ae-running-progress {
  0% { margin-left: 0px; margin-right: 100%; }
  50% { margin-left: 25%; margin-right: 0%; }
  100% { margin-left: 100%; margin-right: 0; }
}

@keyframes ae-running-progress {
  0% { margin-left: 0px; margin-right: 100%; }
  50% { margin-left: 25%; margin-right: 0%; }
  100% { margin-left: 100%; margin-right: 0; }
}
"""


class Mixin:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        set_hook.mixin_helper(cls, Mixin)

    def __init__(self, **properties):
        self.dom_node = anvil.js.get_dom_node(self)
        self.set_var = self.dom_node.firstChild.style.setProperty

    @set_hook
    def on_set_height(self):
        self.set_var("--ae-bar-height", _css_length(self.height or 3))

    @set_hook
    def on_set_track_colour(self):
        self.set_var(
            "--ae-track-color", self.track_colour and _get_color(self.track_colour)
        )

    @set_hook
    def on_set_indicator_colour(self):
        self.set_var("--ae-indicator-color", _get_color(self.indicator_colour))
