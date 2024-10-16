# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js import get_dom_node
from anvil.js.window import setTimeout

from ...popover import pop
from ..Option import Option
from ._anvil_designer import DropDownTemplate

__version__ = "3.0.0"


class DropDown(DropDownTemplate):
    def __init__(self, **properties):
        self._dom_node = get_dom_node(self)
        self._dom_node.style.height = "100%"
        self._props = properties
        self.dd_node = self.dom_nodes["ae-ms-dd"]
        self.options_node = self.dom_nodes["ae-ms-options"]
        self.init_components(**properties)
        self.select_all_btn.role = "ae-ms-select-btn"
        self.deselect_all_btn.role = "ae-ms-select-btn"
        self.filter_box.role = "ae-ms-filter"
        self.dd_node.addEventListener("keydown", self._on_keydown)
        self._no_options = Option()
        self._no_options.visible = False
        self.options_panel.add_component(self._no_options)

    @property
    def options(self):
        return self._props.get("options", [])

    @options.setter
    def options(self, val):
        val = val or []
        self._props["options"] = val
        self.options_panel.clear()
        for opt in val:
            self.options_panel.add_component(opt)
            opt.add_event_handler("click", self._on_option_clicked)

        self.options_panel.add_component(self._no_options)
        self._no_options.visible = False

    @property
    def enable_filtering(self):
        return self._props.get("enable_filtering", False)

    @enable_filtering.setter
    def enable_filtering(self, val):
        self._props["enable_filtering"] = val
        self.filter_box.visible = val

    @property
    def enable_select_all(self):
        return self._props.get("enable_select_all", False)

    @enable_select_all.setter
    def enable_select_all(self, val):
        self._props["enable_select_all"] = val
        self.select_all_flow.visible = self.multiple and val

    @property
    def multiple(self):
        return self._props.get("multiple", False)

    @multiple.setter
    def multiple(self, val):
        self._props["multiple"] = val
        if val:
            self.enable_select_all = self.enable_select_all

    def _close(self):
        pop(self.popper, "hide")

    def _on_filter_show(self, **event_args):
        # because of weird way we are hacking the show events in popovers
        setTimeout(self.filter_box.focus)

    def _on_filter_hide(self, **event_args):
        self.filter_box.text = ""
        for option in self.options:
            option.visible = True

        self._no_options.visible = False

    def _on_filter_change(self, **event_args):
        term = self.filter_box.text or ""
        term = term.lower()
        num_results = 0
        for option in self.options:
            if option.is_divider:
                option.visible = not term
            else:
                visible = term in option.key.lower() or term in option.subtext.lower()
                option.visible = visible
                num_results += visible

        active_idx = self._get_active_idx()
        if active_idx != -1:
            self.options[active_idx].active = False

        no_options = not num_results and term
        self._no_options.visible = no_options
        if no_options:
            self._no_options.label.text = f"No results matched {term!r}"

        if not term:
            return

        first_idx = self._get_next_idx(-1)
        if first_idx != -1:
            self.options[first_idx].active = True

    def _on_filter_enter(self, **e):
        active_idx = self._get_active_idx()
        if active_idx != -1:
            self.options[active_idx].click()

    def _on_select_all(self, **event_args):
        for option in self.options:
            option.selected = True
        self._on_focus()
        self.raise_event("change")

    def _on_deselect_all(self, **event_args):
        for option in self.options:
            option.selected = False
        self._on_focus()
        self.raise_event("change")

    def _on_show(self, **event_args):
        if self.enable_filtering:
            return

        def focus():
            self.options_node.tabIndex = 0
            self.options_node.focus()
            self.options_node.tabIndex = -1

        setTimeout(focus)

    def _on_focus(self, *args, **kws):
        setTimeout(self.filter_box.focus)

    def _get_active_idx(self):
        for i, opt in enumerate(self.options):
            if opt.is_divider:
                continue
            if opt.active:
                return i
        return -1

    def _get_next_idx(self, active_idx, dir=1, pred=None):
        num_options = len(self.options)
        if active_idx == -1 and dir == -1:
            active_idx = 0

        nxt_idx = (active_idx + dir) % num_options

        for i in range(nxt_idx, dir * num_options + nxt_idx, dir):
            idx = i % num_options
            nxt = self.options[idx]
            if nxt.is_divider:
                continue
            if not nxt.visible or nxt.disabled:
                continue
            if pred is None:
                return idx
            cond = pred(nxt)
            if cond:
                return idx

        return -1

    def _on_keydown(self, e):
        key = e.key
        if key == "Tab":
            key = "ArrowUp" if e.shiftKey else "ArrowDown"

        is_input = e.target.nodeName == "INPUT"

        if key == "Escape":
            self._close()
            get_dom_node(self.popper).firstElementChild.focus()
            # TODO focus the popper

        elif key == " ":
            if not is_input:
                e.preventDefault()

        elif key == "Enter":
            e.preventDefault()
            self._on_filter_enter()

        elif key == "ArrowDown" or key == "ArrowUp":
            e.preventDefault()

            dir = 1 if key == "ArrowDown" else -1
            active_idx = self._get_active_idx()
            if active_idx != -1:
                self.options[active_idx].active = False
            next_idx = self._get_next_idx(active_idx, dir)
            if next_idx != -1:
                self.options[next_idx].active = True

        elif key.isalpha():
            if is_input:
                return
            key = key.lower()
            active_idx = self._get_active_idx()
            next_idx = self._get_next_idx(
                active_idx, dir=1, pred=lambda opt: opt.key.lower().startswith(key)
            )
            if next_idx != -1:
                if active_idx != -1:
                    self.options[active_idx].active = False
                self.options[next_idx].active = True

    def _on_option_clicked(self, sender, **e):
        multiple = self.multiple
        for opt in self.options:
            if not multiple:
                opt.selected = opt is sender
            opt.active = opt is sender and not sender.disabled

        if sender.disabled:
            return

        self.raise_event("change")

        if not self.multiple:
            self._close()
