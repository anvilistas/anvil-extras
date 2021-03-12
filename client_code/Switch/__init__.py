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
from .. import session
from ._anvil_designer import SwitchTemplate

__version__ = "1.0.0"

css = """
.anvil-role-switch {
   position: relative;
   width: 1.8em;
}

.anvil-role-switch input { 
  opacity: 0;
  height: 0;
}

.anvil-role-switch span {
   position: relative;
   display: block !important;
   font-size: ineherit;
}

.anvil-role-switch span::before {
   content: "";
   position: absolute;
   cursor: pointer;
   top: 0.1em;
   bottom: 0;
   left: -1em;
   width: 1.8em;
   height: 1em;
   background-color: #ccc;
   -webkit-transition: .4s;
   transition: .4s;
}

.anvil-role-switch span::after {
   position: absolute;
   cursor: pointer;
   content: "";
   height: .8em;
   width: .8em;
   left: -.88em;
   top: .2em;
   bottom: 0;
   background-color: white;
   -webkit-transition: .4s;
   transition: .4s;
}

.anvil-role-switch input:checked + span::after {
 -webkit-transform: translateX(.8em);
 -ms-transform: translateX(.8em);
 transform: translateX(.8em);
}

.anvil-role-switch span::after {
 border-radius: 50%;
}
.anvil-role-switch span::before {
 border-radius: .5em;
}
"""
session.style_injector.inject(css)


class Switch(SwitchTemplate):
    def __init__(self, checked_colour, **properties):
        self.uid = session.get_uid()
        self._checked = False
        css = f"""
.anvil-role-switch-{self.uid} input:checked + span::before {{
 background-color: {checked_colour};
}}

.anvil-role-switch-{self.uid} input:focus + span::before {{
 box-shadow: 0 0 1px {checked_colour};
}}
"""
        session.style_injector.inject(css)
        self.check_box.role = ["switch", f"switch-{self.uid}"]
        self.init_components(**properties)
        
    @property
    def checked(self):
        return self._checked
      
    @checked.setter
    def checked(self, value):
        self._checked = value
        self.refresh_data_bindings()
        self.raise_event("changed")
