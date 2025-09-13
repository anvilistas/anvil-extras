# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import LinearPanel as _LinearPanel
from anvil import Link as _Link
from anvil import pluggable_ui as _pluggable_ui
from anvil.designer import get_design_component
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import document as _document
from anvil.js.window import jQuery as _S
from anvil.js.window import window as _window

from ..utils._component_helpers import _html_injector
from ..virtualize import Virtualizer

__version__ = "3.4.0"


_html_injector.css(
    """
.anvil-role-ae-autocomplete {
    padding: 0 !important;
}
.anvil-role-ae-autocomplete > ul {
    position: relative;
}
.anvil-role-ae-autocomplete > ul > li {
    position: absolute;
    width: 100%;
    left: 0;
    right: 0;
}
.anvil-role-ae-autocomplete {
    position: absolute;
    transform: scaleX(1) scaleY(1);
    opacity: 1;
    transform-origin: 0px 0px;
    overflow-y: auto;
    min-width: 100px;
    max-height: 300px;
    transition: all 100ms ease;
    background-color: #fff;
    border-radius: 2px;
    z-index: 3001;
    box-shadow: 0 2px 2px 0 rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%), 0 1px 5px 0 rgb(0 0 0 / 20%);
}
.anvil-role-ae-autocomplete.visible-false, .anvil-role-ae-autocomplete.anvil-visible-false {
    transform: scaleX(0) scaleY(0);
    opacity: 0;
    display: block !important;
    transition: all 200ms ease;
}
.anvil-role-ae-autocomplete a {
    padding: 7px 16px;
}
.anvil-role-ae-autocomplete a:hover, .anvil-role-ae-autocomplete a.anvil-role-ae-autocomplete-active {
    background-color: #eee;
}
"""
)


TB = _pluggable_ui["anvil.TextBox"]

# the pluggable ui component might be a callable rather than a class
TB_Class = type(TB())


AUTOCOMPLETE_PROPS = [
    {
        "name": "suggestions",
        "type": "text[]",
        "description": "The list of suggestions to display",
        "default_value": [],
        "group": "autocomplete",
        "important": True,
        "priority": 100,
    },
    {
        "name": "suggest_if_empty",
        "type": "boolean",
        "description": "Whether to suggest suggestions when the text is empty",
        "default_value": True,
        "group": "autocomplete",
        "important": True,
    },
    {
        "name": "filter_mode",
        "type": "enum",
        "description": "How the autocompletion should filter suggestions",
        "options": ["contains", "startswith"],
        "default_value": "contains",
        "group": "autocomplete",
        "important": True,
    },
]

TB_PROPS = TB_Class._anvil_properties_


class Autocomplete(get_design_component(TB_Class)):
    _anvil_properties_ = AUTOCOMPLETE_PROPS + TB_PROPS
    _anvil_events_ = [
        {"name": "suggestion_clicked"},
        {"name": "pressed_enter", "defaultEvent": True},
        {"name": "focus"},
        {"name": "lost_focus"},
        {"name": "change"},
    ]

    def __init__(self, **properties):

        self._active_nodes = []
        self.__active = None
        self.__active_index = -1
        self.__link_height = 0
        self.__nodes = {}
        self.__filter_mode = None
        self.__filter_fn = self.__filter_contains

        self.__lp = _LinearPanel(
            role="ae-autocomplete",
            spacing_above="none",
            spacing_below="none",
            visible=False,
        )
        self.__lp_node = _get_dom_node(self.__lp)

        dom_node = self.__dom_node = _get_dom_node(self)
        if dom_node.tagName != "INPUT":
            dom_node = self.__dom_node = dom_node.querySelector("input")

        tb_props = {
            k: v
            for k, v in properties.items()
            if any(prop["name"] == k for prop in TB_PROPS)
        }
        super().__init__(**tb_props)

        for prop in AUTOCOMPLETE_PROPS:
            setattr(self, prop["name"], properties.get(prop["name"]))

        # use capture for keydown so we can get the event before anvil does
        dom_node.addEventListener("keydown", self.__on_keydown, True)
        dom_node.addEventListener("input", self.__on_input)
        dom_node.addEventListener("focus", self.__on_focus, True)
        dom_node.addEventListener("blur", self.__on_blur)
        self.set_event_handler("x-popover-init", self.__handle_popover)
        self.set_event_handler("x-popover-destroy", self.__handle_popover)
        self.add_event_handler("x-anvil-page-added", self.__on_show)
        self.add_event_handler("x-anvil-page-removed", self.__on_hide)

        self.__virtualizer = Virtualizer(
            count=0,
            estimate_size=lambda idx: 48,
            component=self,
            scroll_element=self.__lp_node,
            on_change=self.__populate,
        )

    ###### PRIVATE METHODS ######
    @staticmethod
    def __filter_contains(text, search):
        return text.lower().find(search)

    @staticmethod
    def __filter_startswith(text, search):
        return 0 if text.lower().startswith(search) else -1

    def __gen_active_nodes(self):
        prev_active = self.__active
        self.__reset_autocomplete()

        search_term = self.text.lower()
        if not search_term and not self.suggest_if_empty:
            return

        n = len(search_term)
        filter_fn = self.__filter_fn

        def get_node_with_emph(text):
            i = filter_fn(text, search_term)
            if i == -1:
                return False
            node = self.__get_node(text)
            if n:
                node.tag.innerHTML = (
                    text[:i] + "<b>" + text[i : i + n] + "</b>" + text[i + n :]
                )
            return node

        self.__active_nodes = [
            node for node in map(get_node_with_emph, self.suggestions) if node
        ]
        try:
            self.__active_index = self.__active_nodes.index(prev_active)
            self.__active = prev_active
            self.__active.role = "ae-autocomplete-active"
        except ValueError:
            pass

        self.__virtualizer.update(count=len(self.__active_nodes))

    def __populate(self):
        self.__lp.clear()

        self.__lp_node.firstElementChild.style.height = (
            f"{self.__virtualizer.get_total_size()}px"
        )

        for item in self.__virtualizer.get_virtual_items():
            node = self.__active_nodes[item.index]
            if node.parent is not None:
                print(f"Warning: you have duplicate suggestions - ignoring {node.text}")
                continue
            self.__lp.add_component(node)
            _get_dom_node(node).parentElement.style.top = f"{item.start}px"

        self.__lp.visible = bool(self.__active_nodes)

    def __get_node(self, text):
        link = self.__nodes.get(text)
        if link:
            link.text = link.text
            return link

        link = _Link(text=text, spacing_above="none", spacing_below="none")
        link.set_event_handler("click", self.__set_text)
        l_node = _get_dom_node(link)
        link.tag = l_node.querySelector("div")
        # this stops the lost_focus event firing when a suggestion is clicked
        l_node.addEventListener("mousedown", lambda e: e.preventDefault())

        self.__nodes[text] = link
        return link

    def __set_text(self, sender=None, *e, **e_args):
        if sender is not None:
            self.text = sender.text
            self.__reset_autocomplete()
            self.raise_event("suggestion_clicked")
        elif self.__active is not None:
            self.text = self.__active.text
            self.__reset_autocomplete()
        else:
            self.__reset_autocomplete()

    def __reset_autocomplete(self):
        if self.__active is not None:
            self.__active.role = None
        self.__active = None
        self.__lp.visible = False
        self.__active_nodes = []
        self.__active_index = -1
        self.__lp_node.scrollTop = 0
        self.__virtualizer.update(count=0)

    def __reset_position(self, *e):
        rect = self.__dom_node.getBoundingClientRect()
        root_rect = _document.documentElement.getBoundingClientRect()
        body_rect = _document.body.getBoundingClientRect()
        fixed_offset_top = body_rect.top - root_rect.top
        lp_node = self.__lp_node
        lp_node.style.left = f"{rect.left - body_rect.left}px"
        lp_node.style.top = f"{rect.bottom - body_rect.top + fixed_offset_top + 5}px"
        lp_node.style.width = f"{rect.width}px"

    ###### INTERNAL EVENTS ######
    def __on_keydown(self, e):
        key = getattr(e, "key", None)
        if key in ("ArrowDown", "ArrowUp"):
            e.preventDefault()
        elif key == "Enter":
            self.__set_text()
            return
        elif key == "Escape":
            self.__reset_autocomplete()
            return
        else:
            return

        try:
            if key == "ArrowDown":
                i = min(self.__active_index + 1, len(self.__active_nodes) - 1)
                new_active = self.__active_nodes[i]
            else:
                i = max(self.__active_index - 1, -1)
                new_active = None if i == -1 else self.__active_nodes[i]
        except IndexError:
            return

        self.__active_index = i
        if self.__active is not None:
            self.__active.role = None
        if new_active is not None:
            new_active.role = "ae-autocomplete-active"
            self.__virtualizer.scroll_to_index(i)

        self.__active = new_active

    def __on_input(self, e):
        """This method is called when the text in this text box is edited"""
        self.__gen_active_nodes()
        self.__populate()

    def __on_focus(self, e):
        """This method is called when the TextBox gets focus"""
        self.__reset_position()
        self.__gen_active_nodes()
        self.__populate()

    def __on_blur(self, e):
        """This method is called when the TextBox loses focus"""
        self.__reset_autocomplete()

    def __on_show(self, **e_args):
        """This method is called when the TextBox is shown on the screen"""
        _document.body.appendChild(self.__lp_node)
        _S(_window).on("resize", self.__reset_position)

    def __on_hide(self, **e_args):
        """This method is called when the TextBox is removed from the screen"""
        try:
            self.__lp_node.remove()
        except Exception:
            pass
        _S(_window).off("resize", self.__reset_position)
        self.__nodes = {}

    def __handle_popover(self, init_node, **event_args):
        init_node(self.__lp_node)

    ##### Properties ######
    @property
    def suggestions(self):
        return self.__data or []

    @suggestions.setter
    def suggestions(self, val):
        self.__data = val
        if self.__dom_node is _document.activeElement:
            self.__gen_active_nodes()
            self.__populate()

    @property
    def filter_mode(self):
        return self.__filter_mode

    @filter_mode.setter
    def filter_mode(self, value):
        self.__filter_mode = value
        if value == "startswith":
            self.__filter_fn = self.__filter_startswith
        else:
            self.__filter_fn = self.__filter_contains
