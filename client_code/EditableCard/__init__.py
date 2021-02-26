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
import datetime as dt
from copy import deepcopy

from ._anvil_designer import EditableCardTemplate

__version__ = "0.1.5"

day_format = "%d/%m/%Y"
time_format = "%I.%M %p"


class EditableCard(EditableCardTemplate):
    def __init__(self, **properties):
        self._item = {"name": None, "value": None, "title": None}
        self._icon = None
        self.original_item = None
        self.changed = False
        self.background_colours = {True: "#cac5fb", False: "white"}
        self.hours_dropdown.items = [f"{h:02d}" for h in range(1, 13)]
        self.minutes_dropdown.items = [f"{m:02d}" for m in range(0, 60)]
        self.yesno_dropdown.items = [("", ""), ("Yes", "yes"), ("No", "no")]
        self.init_components(**properties)

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        self.original_item = deepcopy(value)
        self.value_text_box.placeholder = str(value)
        self._item = value
        self.refresh_data_bindings()

    @property
    def text(self):
        return str(self.item)

    @text.setter
    def text(self, value):
        self.changed = value != self.item["value"]
        self.item["value"] = value
        if self.changed:
            self.raise_event("x-item-changed", item=self.item)
        self.value_text_box.placeholder = str(self.item)
        self.value_text_box.text = ""
        self.refresh_data_bindings()

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.refresh_data_bindings()

    @property
    def text_box_type(self):
        return "number" if self.datatype == "number" else "text"

    @property
    def pick_time(self):
        return True if self.datatype == "time" else False

    def _edit_text(self):
        self.value_text_box.placeholder = ""
        self.value_text_box.text = self.text

    def _edit_date(self):
        self.text_box_column_panel.visible = False
        self.date_picker_column_panel.visible = True

    def _edit_time(self):
        self.hours_dropdown.selected_value = self.text.split(".")[0]
        self.minutes_dropdown.selected_value = self.text.split(".")[1][:2]
        self.am_pm_dropdown.selected_value = self.text[-2:]
        self.text_box_column_panel.visible = False
        self.time_picker_column_panel.visible = True

    def _edit_yesno(self):
        self.text_box_column_panel.visible = False
        self.yesno_column_panel.visible = True

    def value_text_box_focus(self, sender, **event_args):
        actions = {
            "text": self._edit_text,
            "number": self._edit_text,
            "date": self._edit_date,
            "time": self._edit_time,
            "yesno": self._edit_yesno,
        }
        actions[self.datatype]()

    def value_text_box_lost_focus(self, sender, **event_args):
        sender.placeholder = self.text
        sender.text = ""

    def value_text_box_pressed_enter(self, sender, **event_args):
        self.text = sender.text or ""

    def undo_link_click(self, **event_args):
        self.text = self.original_item["value"]
        self.changed = False
        self.refresh_data_bindings()

    def date_picker_change(self, sender, **event_args):
        self.date_picker_column_panel.visible = False
        self.text_box_column_panel.visible = True
        self.text = sender.date

    def cancel_time_button_click(self, **event_args):
        self.time_picker_column_panel.visible = False
        self.text_box_column_panel.visible = True

    def apply_time_button_click(self, **event_args):
        self.time_picker_column_panel.visible = False
        self.text_box_column_panel.visible = True
        hours = int(self.hours_dropdown.selected_value)
        if self.am_pm_dropdown.selected_value == "PM":
            hours += 12
        minutes = int(self.minutes_dropdown.selected_value)
        self.text = dt.time(hours, minutes)

    def yesno_dropdown_change(self, sender, **event_args):
        self.yesno_column_panel.visible = False
        self.text_box_column_panel.visible = True
        self.text = sender.selected_value
