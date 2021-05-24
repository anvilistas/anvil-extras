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

from anvil import CheckBox, app
from anvil.js import get_dom_node as _get_dom_node

from .. import session

__version__ = "1.0.0"

primary = app.theme_colors.get("Primary 500", "#2196F3")

css = """
.anvil-switch label {
  padding: 0 !important;
}

.anvil-switch .checkbox {
  display: flex;
  align-items: center;
}

.anvil-switch input {
  opacity: 0;
  height: 0;
  margin-top: 0 !important;
}

.anvil-switch span {
  position: relative;
  line-height: 1;
  display: flex !important;
  align-items: center;
}

.anvil-switch span::before {
  content: "";
  display: inline-block;
  width: 1.8em;
  height: 1em;
  background-color: #ccc;
  -webkit-transition: background-color.4s;
  transition: background-color 0.4s;
  margin-right: 10px;
}

.anvil-switch span::after {
  position: absolute;
  content: "";
  height: 0.8em;
  width: 0.8em;
  background-color: white;
  -webkit-transition: transform 0.4s;
  transition: transform 0.4s;
  margin: 0.1em;
}
.anvil-switch input:checked + span::after {
  -webkit-transform: translateX(0.8em);
  -ms-transform: translateX(0.8em);
  transform: translateX(0.8em);
}

.anvil-switch span::after {
  border-radius: 50%;
}
.anvil-switch span::before {
  border-radius: 0.5em;
}
.anvil-switch input:checked + span::before {
  background-color: var(--color);
}
.anvil-switch input:focus + span::before {
  box-shadow: 0 0 1px var(--color);
}

.anvil-switch[disabled] label {
  cursor: not-allowed;
}
.anvil-switch[disabled] input:checked + span::before {
  opacity: .7;
}

"""
session.style_injector.inject(css)


class Switch(CheckBox):
    def __init__(self, checked_color=primary, **properties):
        self._dom_node = _get_dom_node(self)
        self._dom_node.classList.add("anvil-switch")
        self.checked_color = checked_color or primary

    @property
    def checked_color(self):
        return self._checked_color

    @checked_color.setter
    def checked_color(self, value):
        self._checked_color = value
        dom_node = _get_dom_node(self)
        if value and value.startswith("theme:"):
            value = app.theme_colors.get(value.replace("theme:", ""), primary)
        dom_node.style.setProperty("--color", value)
