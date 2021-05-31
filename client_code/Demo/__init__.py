# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from ..utils import auto_refreshing
from ._anvil_designer import DemoTemplate

__version__ = "1.2.0"


@auto_refreshing
class Demo(DemoTemplate):
    def __init__(self, **properties):
        self.progress = 0
        self.item = self.default_item = dict(
            tally=100, counter=0, values=self.slider.start
        )
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

    ###### MULTI SELECT ######
    def multi_select_drop_down_1_change(self, **event_args):
        """This method is called when the selected values change"""
        print(self.multi_select_drop_down_1.selected)

    ###### QUILL ######
    def quill_text_change(self, **event_args):
        """This method is called when the quill text changes"""
        print(self.quill.get_text())

    ###### SLIDER ######
    def set_text_boxes(self):
        self.text_box_left.text, self.text_box_right.text = self.slider.formatted_values

    def slider_button_reset_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.slider.reset()
        self.slider.behaviour = "drag"

    def slider_change(self, handle, **event_args):
        """This method is called when the slider has finished sliding"""
        print(
            f"change\nhandle={handle} | value={self.slider.values[handle]} | formatted={self.slider.formatted_values[handle]}"
        )

    def slider_slide(self, handle, **event_args):
        """This method is called when the slider is sliding or dragging"""
        self.set_text_boxes()
        print(
            f"slide\nhandle={handle} | value={self.slider.values[handle]} | formatted={self.slider.formatted_values[handle]}"
        )

    def slider_textbox_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.slider.values = self.text_box_left.text, self.text_box_right.text
        self.set_text_boxes()
