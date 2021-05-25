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
from ..utils import auto_refreshing
from ._anvil_designer import DemoTemplate

__version__ = "1.2.0"


@auto_refreshing
class Demo(DemoTemplate):
    def __init__(self, **properties):
        self.progress = 0
        self.item = self.default_item = dict(tally=100, counter=0)
        self.init_components(**properties)

    def timer_1_tick(self, **event_args):
        if self.progress <= 1:
            self.progress_bar.progress = self.progress
            self.progress += 0.01
        else:
            self.timer_1.interval = 0

    def minus_button_click(self, **event_args):
        self.item["tally"] -= 1
        self.item["counter"] += 1

    def plus_button_click(self, **event_args):
        self.item["tally"] += 1
        self.item["counter"] += 1

    def reset_button_click(self, **event_args):
        self.item = self.default_item

    def multi_select_drop_down_1_change(self, **event_args):
        """This method is called when the selected values change"""
        print(self.multi_select_drop_down_1.selected)

    def quill_text_change(self, **event_args):
        """This method is called when the quill text changes"""
        print(self.quill.get_text())
