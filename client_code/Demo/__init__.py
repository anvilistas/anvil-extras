# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
import anvil.http

from ..utils import auto_refreshing
from ._anvil_designer import DemoTemplate

__version__ = "2.2.3"
dataset_url = "https://pivottable.js.org/examples/mps.json"


#### AUTO REFRESING - the item property updates components
@auto_refreshing
class Demo(DemoTemplate):
    def __init__(self, **properties):
        self.init_custom_slider_formatter()

        self.progress = 0
        self.default_item = dict(
            tally=100,
            counter=0,
            values=self.slider.start,
            agree=self.slider_agree.value,
            chips=["a", "b", "c"],
            text="",
        )
        self.item = self.default_item.copy()
        self.pivot.items = anvil.http.request(dataset_url, json=True)
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
        self.item = self.default_item.copy()

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

    ###### SLIDER WITH CUSTOM FORMATTER
    def init_custom_slider_formatter(self):
        num_to_desc = {
            -5: "strongly disagree",
            -2.5: "disagree",
            0: "neutral",
            2.5: "agree",
            5: "strongly agree",
        }

        desc_to_num = {v: k for k, v in num_to_desc.items()}

        self.slider_agree.format = {
            # to should return a str
            "to": lambda num: num_to_desc.get(num, str(num)),
            # from should return a number - if it fails then an attempt will be made to convert the str to float
            "from": lambda desc: desc_to_num[desc],
        }

        ### it's also possible to provide a custom formatter to tooltips - only to is required
        self.slider_agree.tooltips = {"to": lambda num: format(num, ".0f")}

    def slider_agree_change(self, handle, **event_args):
        """This method is called when the slider has finished sliding"""
        print("slider changed - value:", self.slider_agree.value)

    def slider_down_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.slider_agree.value -= 1
        self.update_item_agree()

    def slider_reset_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.slider_agree.reset()
        self.update_item_agree()

    def slider_up_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.slider_agree.value += 1
        self.update_item_agree()

    def update_item_agree(self):
        """This method is called when the slider values are updated from code"""
        self.item["agree"] = self.slider_agree.value
        print("slider set - value:", self.slider_agree.value)

    def tabs_1_tab_click(self, tab_index, tab_title, **event_args):
        """This method is called when a tab is clicked"""
        self.tabs_label.text = f"{tab_title} is visible"

    def chips_1_chips_changed(self, **event_args):
        """This method is called when a chip is added or removed"""
        print(self.item["chips"])

    def autocomplete_event(self, event_name, **event_args):
        print(event_name, self.item["text"])
