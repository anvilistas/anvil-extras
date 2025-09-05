# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js import get_dom_node
from anvil.js.window import document as _document
from anvil.js.window import setTimeout

from ...logging import DEBUG as _DEBUG
from ...logging import TimerLogger as _TimerLogger
from ...popover import pop
from ..Option import Option
from ._anvil_designer import DropDownTemplate

__version__ = "3.3.0"


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
        # backing store for html-rendered options (list of dicts)
        self._options_data = []
        # event delegation listeners
        self.options_node.addEventListener("click", self._on_click_delegate)

    @property
    def options(self):
        return self._options_data

    @options.setter
    def options(self, val):
        # val is list of dicts produced by parent component
        val = val or []
        self._options_data = val
        # timing instrumentation
        tlog = _TimerLogger(name="ms-dd.options", level=_DEBUG)
        try:
            tlog.start("options: start")
        except Exception:
            pass

        # clear container
        self.options_node.innerHTML = ""
        try:
            tlog.check("cleared panel")
        except Exception:
            pass

        # build a single HTML string for all options
        html_parts = ['<div class="ae-ms-options-wrap"><ul>']
        for idx, opt in enumerate(val):
            if opt.get("is_divider"):
                html_parts.append("<li><div data-divider></div></li>")
                continue
            key = opt.get("key", "")
            title = opt.get("title") or key
            subtext = opt.get("subtext") or ""
            icon = opt.get("icon") or ""
            disabled = opt.get("disabled", False)
            selected = opt.get("selected", False)
            classes = ["anvil-role-ae-ms-option"]
            if selected:
                classes.append("anvil-role-ae-ms-option-selected")
            cls = " ".join(classes)
            data_disabled = ' data-disabled=""' if disabled else ""
            # icon mapping for FA4: accept "fa:foo" or "far:foo" and map to "fa fa-foo"
            icon_html = ""
            if icon:
                try:
                    prefix, name = icon.split(":", 1)
                except ValueError:
                    name = icon
                name = name.strip().replace(" ", "-")
                if name and not name.startswith("fa-"):
                    name = f"fa-{name}"
                icon_html = (
                    f'<i class="ae-ms-option-icon fa {name}" aria-hidden="true"></i>'
                )
            # right-side check placeholder (always present; visibility via CSS)
            # icon and subtext inline with label
            label_html = (
                f'<div class="anvil-role-ae-ms-option-label">'
                f"{icon_html}"
                f'<span class="ae-ms-label-text">{title}</span>'
                f'<span class="ae-ms-subtext">{subtext}</span>'
                f"</div>"
            )
            html_parts.append(
                f'<li><a class="{cls}" data-idx="{idx}" data-key="{key}" tabindex="-1"{data_disabled}>'
                f"{label_html}"
                f'<i class="ae-ms-chk fa fa-check" aria-hidden="true"></i>'
                f"</a></li>"
            )
        html_parts.append("</ul></div>")
        self.options_node.innerHTML = "".join(html_parts)

        try:
            tlog.check(f"added components (n={len(val)})")
        except Exception:
            pass
        try:
            tlog.end("options: end")
        except Exception:
            pass

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
        # show all
        for el in self._iter_option_elements():
            el.parentElement.style.display = ""

    def _on_filter_change(self, **event_args):
        term = self.filter_box.text or ""
        term = term.lower()
        num_results = 0
        for idx, opt in enumerate(self._options_data):
            el = self._get_option_element(idx)
            if el is None:
                continue
            if opt.get("is_divider"):
                el.parentElement.style.display = "none" if term else ""
                continue
            key = (opt.get("key") or "").lower()
            sub = (opt.get("subtext") or "").lower()
            visible = (term in key) or (term in sub)
            el.parentElement.style.display = "" if visible else "none"
            num_results += 1 if visible else 0

        # clear active
        self._set_active_idx(-1)

        if not term:
            return

        first_idx = self._get_next_idx(-1)
        if first_idx != -1:
            self._set_active_idx(first_idx)

    def _on_filter_enter(self, **e):
        active_idx = self._get_active_idx()
        if active_idx != -1:
            self._on_option_clicked(active_idx)

    def _on_select_all(self, **event_args):
        for option in self._options_data:
            if not option.get("is_divider") and not option.get("disabled"):
                option["selected"] = True
        self._on_focus()
        self.raise_event("change")
        self._sync_dom_selection()

    def _on_deselect_all(self, **event_args):
        for option in self._options_data:
            if not option.get("is_divider"):
                option["selected"] = False
        self._on_focus()
        self.raise_event("change")
        self._sync_dom_selection()

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
        for i, opt in enumerate(self._options_data):
            if opt.get("is_divider"):
                continue
            el = self._get_option_element(i)
            if el is not None and "anvil-role-ae-ms-option-active" in el.classList:
                return i
        return -1

    def _get_next_idx(self, active_idx, dir=1, pred=None):
        num_options = len(self._options_data)

        if num_options == 0:
            return -1

        if active_idx == -1 and dir == -1:
            active_idx = 0

        nxt_idx = (active_idx + dir) % num_options

        for i in range(nxt_idx, dir * num_options + nxt_idx, dir):
            idx = i % num_options
            nxt = self._options_data[idx]
            if nxt.get("is_divider"):
                continue
            el = self._get_option_element(idx)
            if (
                el is None
                or el.parentElement.style.display == "none"
                or nxt.get("disabled")
            ):
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
                self._set_active_idx(-1)
            next_idx = self._get_next_visible_idx(active_idx, dir)
            if next_idx != -1:
                self._set_active_idx(next_idx)

        elif key.isalpha():
            if is_input:
                return
            key = key.lower()
            active_idx = self._get_active_idx()
            next_idx = self._get_next_visible_idx(
                active_idx,
                dir=1,
                pred=lambda opt: (opt.get("key") or "").lower().startswith(key),
            )
            if next_idx != -1:
                if active_idx != -1:
                    self._set_active_idx(-1)
                self._set_active_idx(next_idx)

    def _on_option_clicked(self, idx):
        """Handle a click on option index idx in _options_data."""
        opt = self._options_data[idx]
        if opt.get("disabled"):
            return
        multiple = self.multiple
        if multiple:
            # Toggle only clicked item
            opt["selected"] = not opt.get("selected", False)
            self._update_dom_selection_for_idx(idx)
        else:
            # Single select: find previous selected (if any) and update only those two indices
            prev_idx = None
            for i, o in enumerate(self._options_data):
                if o.get("selected"):
                    prev_idx = i
                    break
            if prev_idx is not None and prev_idx != idx:
                self._options_data[prev_idx]["selected"] = False
                self._update_dom_selection_for_idx(prev_idx)
            # select current
            self._options_data[idx]["selected"] = True
            self._update_dom_selection_for_idx(idx)
        # ensure active styling follows the clicked row
        try:
            self._set_active_idx(idx)
        except Exception:
            pass
        self.raise_event("change")
        if not multiple:
            self._close()

    # --- helpers for HTML renderer ---
    def _iter_option_elements(self):
        return self.options_node.querySelectorAll(".anvil-role-ae-ms-option")

    def _get_option_element(self, idx):
        return self.options_node.querySelector(
            f'.anvil-role-ae-ms-option[data-idx="{idx}"]'
        )

    def _is_option_focusable(self, idx):
        try:
            opt = self._options_data[idx]
        except Exception:
            return False
        if opt.get("is_divider") or opt.get("disabled"):
            return False
        el = self._get_option_element(idx)
        if el is None:
            return False
        # consider filtered-out items not focusable
        try:
            disp = getattr(el.style, "display", "")
            if disp == "none":
                return False
        except Exception:
            pass
        return True

    def _get_next_visible_idx(self, active_idx, dir=1, pred=None):
        """Find next index in given direction that is focusable and matches pred if provided.
        Wraps around; returns -1 if none found.
        """
        n = len(self._options_data) if hasattr(self, "_options_data") else 0
        if n == 0:
            return -1
        # start point
        i = active_idx
        steps = 0
        while steps < n:
            if i == -1:
                i = 0 if dir > 0 else n - 1
            else:
                i = (i + dir) % n
            steps += 1
            if not self._is_option_focusable(i):
                continue
            if pred is None or pred(self._options_data[i]):
                return i
        return -1

    def _set_active_idx(self, idx):
        # Fast path: toggle only the previously active and the new active element
        prev = getattr(self, "_active_idx", -1)
        if prev != -1 and prev != idx:
            el_prev = self._get_option_element(prev)
            if el_prev is not None:
                el_prev.classList.remove("anvil-role-ae-ms-option-active")
        if idx == -1:
            self._active_idx = -1
            return
        el = self._get_option_element(idx)
        if el is not None:
            el.classList.add("anvil-role-ae-ms-option-active")
            try:
                el.scrollIntoView({"block": "nearest"})
            except Exception:
                pass
        self._active_idx = idx

    def _update_dom_selection_for_idx(self, idx):
        el = self._get_option_element(idx)
        if el is None:
            return
        if self._options_data[idx].get("selected"):
            el.classList.add("anvil-role-ae-ms-option-selected")
        else:
            el.classList.remove("anvil-role-ae-ms-option-selected")

    def _sync_dom_selection(self):
        for idx, opt in enumerate(self._options_data):
            el = self._get_option_element(idx)
            if el is None or opt.get("is_divider"):
                continue
            if opt.get("selected"):
                el.classList.add("anvil-role-ae-ms-option-selected")
            else:
                el.classList.remove("anvil-role-ae-ms-option-selected")

    # event delegation handler
    def _on_click_delegate(self, e):
        target = e.target
        el = (
            target.closest(".anvil-role-ae-ms-option")
            if hasattr(target, "closest")
            else None
        )
        if not el:
            return
        idx = int(el.getAttribute("data-idx") or -1)
        if idx >= 0:
            self._on_option_clicked(idx)
