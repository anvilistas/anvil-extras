# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil.js import get_dom_node, import_from
from anvil.js.window import clearTimeout, document, setTimeout

from ...popover import pop
from ...virtualize import Virtualizer
from ._anvil_designer import DropDownTemplate

__version__ = "3.4.0"

_TEMP_DIV = document.createElement("div")


class DropDown(DropDownTemplate):
    def __init__(self, **properties):
        self._dom_node = get_dom_node(self)
        self._dom_node.style.height = "100%"
        self._props = properties
        self.dd_node = self.dom_nodes["ae-ms-dd"]
        self.options_node = self.dom_nodes["ae-ms-options"]
        self.virt_list = self.dom_nodes["ae-ms-virt-list"]
        self.init_components(**properties)
        self.select_all_btn.role = "ae-ms-select-btn"
        self.deselect_all_btn.role = "ae-ms-select-btn"
        self.filter_box.role = "ae-ms-filter"
        self.dd_node.addEventListener("keydown", self._on_keydown)
        self._max_width = 0
        # backing store for html-rendered options (list of dicts)
        self._options_data = []
        # tracked active index for keyboard navigation
        self._active_idx = -1
        # filter debounce state
        self._filter_timer = None
        self._last_filter_term = ""
        # virtualizer scaffolding
        self._filtered_indexes = []  # maps virtual index -> original index
        # filtering state: list of original indices currently visible
        self._filtered_pos = {}  # maps original index -> virtual index

        self._virtualizer = Virtualizer(
            count=0,
            component=self,
            scroll_element=self.options_node,
            estimate_size=self._estimate_size,  # divider-aware estimate
            on_change=self._render_virtual,
            get_item_key=lambda i: self._filtered_indexes[i],
        )

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
        # cache lowercase search fields to avoid repeated lower() on each keystroke
        for opt in self._options_data:
            key = (opt.get("key") or "").lower()
            sub = (opt.get("subtext") or "").lower()
            opt["_search"] = f"{key} {sub}".strip()
            opt["_visible"] = True

        self._max_width = 0
        self._estimate_max_width()

        self._apply_filter(self._last_filter_term)

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
        setTimeout(self.filter_box.focus, 10)

    def _on_filter_hide(self, **event_args):
        self.filter_box.text = ""
        # show all
        for opt in self._options_data:
            opt["_visible"] = True
        # clear any active element when filter/search UI is hidden
        self._set_active_idx(-1)

    def _on_filter_change(self, **event_args):
        term = (self.filter_box.text or "").lower()
        if term == self._last_filter_term:
            return
        self._last_filter_term = term
        # debounce apply
        clearTimeout(self._filter_timer)
        if not term:
            # run immediately to reset quickly
            self._filter_timer = None
            self._apply_filter(term)
            return

        def _run():
            self._apply_filter(term)

        self._filter_timer = setTimeout(_run, 40)

    def _apply_filter(self, term: str):

        for opt in self._options_data:
            if opt.get("is_divider"):
                opt["_visible"] = False if term else True
                continue
            search = opt.get("_search", "")
            visible = (term in search) if term else True
            opt["_visible"] = visible

        self._recompute_filtered()
        self._render_virtual()

        # update active to first visible item (or clear if none)
        next_idx = self._get_next_visible_idx(-1, dir=1)
        self._set_active_idx(next_idx if next_idx != -1 else -1)

    def _on_filter_enter(self, **e):
        active_idx = self._get_active_idx()
        if active_idx != -1:
            self._on_option_clicked(active_idx)

    def _on_select_all(self, **event_args):
        for option in self._options_data:
            if (
                not option.get("is_divider")
                and not option.get("disabled")
                and option.get("_visible")
            ):
                option["selected"] = True
        self._on_focus()
        self.raise_event("change")
        self._sync_dom_selection()

    def _on_deselect_all(self, **event_args):
        for option in self._options_data:
            if not option.get("is_divider") and option.get("_visible"):
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

        setTimeout(focus, 10)

    def _on_focus(self, *args, **kws):
        setTimeout(self.filter_box.focus)

    def _get_active_idx(self):
        return self._active_idx

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
        return bool(opt.get("_visible", True))

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
        prev = self._get_active_idx()
        if prev != -1 and prev != idx:
            el_prev = self._get_option_element(prev)
            if el_prev is not None:
                el_prev.classList.remove("anvil-role-ae-ms-option-active")
        if idx == -1:
            self._active_idx = -1
            return
        # ensure item is scrolled into view using virtualizer
        # translate original index -> virtual index for scrolling
        vpos = self._filtered_pos.get(idx)
        if vpos is not None:
            self._virtualizer.scroll_to_index(vpos, align="auto")

        el = self._get_option_element(idx)
        if el is not None:
            el.classList.add("anvil-role-ae-ms-option-active")
        self._active_idx = idx
        # After scrolling, focus may revert to <body>. Restore focus to the options container
        self._ensure_keyboard_focus()

    def _recompute_filtered(self):
        """Rebuild the filtered index list and positional map, then update the virtualizer count."""
        # Include all visible rows here (options and dividers). When filtering,
        # _apply_filter() sets dividers to _visible = False, so they are excluded.
        self._filtered_indexes = [
            i for i, opt in enumerate(self._options_data) if opt.get("_visible", True)
        ]
        self._filtered_pos = {
            orig: vi for vi, orig in enumerate(self._filtered_indexes)
        }
        self._virtualizer.update(count=len(self._filtered_indexes))

    def _update_dom_selection_for_idx(self, idx):
        el = self._get_option_element(idx)
        if el is None:
            return
        if self._options_data[idx].get("selected"):
            el.classList.add("anvil-role-ae-ms-option-selected")
        else:
            el.classList.remove("anvil-role-ae-ms-option-selected")

    def _estimate_size(self, v_idx):
        """Estimated row height for virtual index v_idx.
        Dividers are short; options use the default row height.
        """
        orig = self._filtered_indexes[v_idx]
        opt = self._options_data[orig]
        return 19 if opt.get("is_divider") else 32

    def _sync_dom_selection(self):
        # update classes only for rendered items
        for el in self._iter_option_elements():
            try:
                idx = int(el.getAttribute("data-idx") or -1)
            except Exception:
                continue
            if idx < 0 or idx >= len(self._options_data):
                continue
            if self._options_data[idx].get("selected"):
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

    def _render_virtual(self):
        self.virt_list.innerHTML = ""

        total = self._virtualizer.get_total_size()
        self.virt_list.style.height = f"{int(total)}px"

        items = self._virtualizer.get_virtual_items()

        for it in items:
            v_idx = it.index
            if v_idx < 0 or v_idx >= len(self._filtered_indexes):
                continue
            idx = self._filtered_indexes[v_idx]
            opt = self._options_data[idx]
            if not opt.get("_visible", True):
                continue
            if opt.get("is_divider"):
                li = self._make_divider(v_idx=v_idx, top_px=it.start)
            else:
                # Option row via helper (returns LI containing the anchor)
                li = self._make_option_element(opt, idx, v_idx=v_idx, top_px=it.start)
            self.virt_list.appendChild(li)
            width = li.style.width
            li.style.width = "fit-content"
            self._max_width = max(self._max_width, li.offsetWidth)
            li.style.width = width
            if idx == self._get_active_idx():
                li.firstElementChild.classList.add("anvil-role-ae-ms-option-active")

        self.options_node.style.minWidth = f"{int(self._max_width)}px"

        # self._set_active_idx(self._get_active_idx())
        # If focus was lost during render, ensure our container is focusable and focused
        self._ensure_keyboard_focus()

    def _make_divider(self, v_idx=None, top_px=None):
        data_index = "" if v_idx is None else f"data-index={v_idx}"

        _TEMP_DIV.innerHTML = f"""
        <li role="separator" style="width:100%; position:absolute; left:0; right:0; top:{top_px}px" {data_index}>
        <div data-divider></div>
        </li>
        """
        return _TEMP_DIV.firstElementChild

    def _make_option_element(self, opt, idx, v_idx=None, top_px=None):
        key = opt.get("key", "")
        title = opt.get("title") or key
        subtext = opt.get("subtext") or ""
        icon = (opt.get("icon") or "").strip()
        # container LI
        li = document.createElement("li")
        li.setAttribute("data-idx", str(idx))
        li.setAttribute(
            "style", f"width:100%; position:absolute; left:0; right:0; top:{top_px}px"
        )
        # When rendering virtually, position absolutely and add data-index
        if v_idx is not None:
            li.setAttribute("data-index", str(v_idx))

        disabled = "" if not opt.get("disabled") else 'data-disabled=""'
        data_index = "" if v_idx is None else f"data-index={v_idx}"
        selected = "" if not opt.get("selected") else "anvil-role-ae-ms-option-selected"
        active = (
            "" if idx != self._get_active_idx() else "anvil-role-ae-ms-option-active"
        )

        icon_html = ""
        if icon:
            try:
                prefix, name = icon.split(":", 1)
            except ValueError:
                name = icon
                prefix = "fa"
            name = name.strip().replace(" ", "-")
            if name and not name.startswith("fa-"):
                name = f"fa-{name}"
            icon_html = (
                f'<i class="ae-ms-option-icon {prefix} {name}" aria-hidden="true"></i>'
            )

        _TEMP_DIV.innerHTML = f"""
        <li style="width:100%; position:absolute; left:0; right:0; top:{top_px}px" {data_index}>
<a class="anvil-role-ae-ms-option {selected} {active}" data-idx="{idx}" data-key="{key}" tabindex="-1" {disabled}>
    <div class="anvil-role-ae-ms-option-label">
        {icon_html}
        <span>{title}</span>
        <div class="anvil-role-ae-ms-option-subtext"><span>{subtext}</span></div>
    </div>
    <i class="ae-ms-chk fa fa-check" aria-hidden="true"></i>
</a>
</li>
"""
        return _TEMP_DIV.firstElementChild

    def _ensure_keyboard_focus(self):
        """Ensure keydown continues to be received after scroll/renders.
        We prefer to keep focus within the options container so Arrow keys work.
        """
        active = document.activeElement

        if active and self.dd_node.contains(active):
            return

        cur = self._get_active_idx()
        if cur != -1:
            a = self._get_option_element(cur)
            if a:
                a.focus({"preventScroll": True})
                return

        prev_tab = getattr(self.options_node, "tabIndex", -1)
        self.options_node.tabIndex = 0
        self.options_node.focus({"preventScroll": True})
        self.options_node.tabIndex = prev_tab

    def _estimate_max_width(self):

        candidate = {"opt": None, "idx": -1, "total": -1}
        for i, opt in enumerate(self._options_data):
            if opt.get("is_divider"):
                continue
            total = len(opt.get("key", "")) + len(opt.get("subtext", ""))
            if opt.get("icon"):
                total += 2

            if total > candidate["total"]:
                candidate["opt"] = opt
                candidate["idx"] = i
                candidate["total"] = total

        if candidate["idx"] != -1:
            copy = self._dom_node.cloneNode(True)
            ul = copy.querySelector("ul")
            li = self._make_option_element(candidate["opt"], candidate["idx"])
            ul.appendChild(li)
            li.style.width = "fit-content"
            document.body.appendChild(copy)
            width = li.offsetWidth
            copy.remove()

            self._max_width = max(self._max_width, width)

        self.options_node.style.minWidth = f"{int(self._max_width)}px"

        return self._max_width + 28
