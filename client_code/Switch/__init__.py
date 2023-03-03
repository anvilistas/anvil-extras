# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from anvil import CheckBox, app
from anvil.js import get_dom_node as _get_dom_node
from anvil.js.window import document as _document

from ..utils._component_helpers import _get_rgb, _html_injector

__version__ = "2.2.3"

primary = app.theme_colors.get("Primary 500", "#2196F3")

css = """
.switch,
.switch * {
    -webkit-tap-highlight-color: transparent;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.switch label {
    cursor: pointer;
}

.switch label input[type=checkbox] {
    opacity: 0;
    width: 0;
    height: 0;
}
.switch label input[type=checkbox]:checked+.lever {
    background-color: rgba(var(--color), .5);
}
.switch label input[type=checkbox]:checked+.lever:after,
.switch label input[type=checkbox]:checked+.lever:before {
    left: 18px;
}
.switch label input[type=checkbox]:checked+.lever:after {
    background-color: rgb(var(--color));
}

.switch label .lever {
    content: "";
    display: inline-block;
    position: relative;
    width: 36px;
    height: 14px;
    background-color: rgba(0,0,0,0.38);
    border-radius: 15px;
    margin-right: 10px;
    -webkit-transition: background 0.3s ease;
    transition: background 0.3s ease;
    vertical-align: middle;
    margin: 0 16px;
}
.switch label .lever:after,
.switch label .lever:before {
    content: "";
    position: absolute;
    display: inline-block;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    left: 0;
    top: -3px;
    -webkit-transition: left 0.3s ease, background 0.3s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease;
    transition: left 0.3s ease, background 0.3s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease;
    transition: left 0.3s ease, background 0.3s ease, box-shadow 0.1s ease, transform 0.1s ease;
    transition: left 0.3s ease, background 0.3s ease, box-shadow 0.1s ease, transform 0.1s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease;
}
.switch label .lever:before {
    background-color: rgb(var(--color), 0.15);
}
.switch label .lever:after {
    background-color: #F1F1F1;
    -webkit-box-shadow: 0 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0 rgba(0,0,0,0.14),0px 1px 5px 0 rgba(0,0,0,0.12);
    box-shadow: 0 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0 rgba(0,0,0,0.14),0px 1px 5px 0 rgba(0,0,0,0.12);
}
input[type=checkbox]:checked:not(:disabled) ~ .lever:active::before,
input[type=checkbox]:checked:not(:disabled).tabbed:focus ~ .lever::before {
    -webkit-transform: scale(2.4);
    transform: scale(2.4);
    background-color: rgb(var(--color), 0.15);
}
input[type=checkbox]:not(:disabled) ~ .lever:active:before,
input[type=checkbox]:not(:disabled).tabbed:focus ~ .lever::before {
    -webkit-transform: scale(2.4);
    transform: scale(2.4);
    background-color: rgba(0,0,0,0.08);
}

.switch input[type=checkbox][disabled]+.lever {
    cursor: default;
    background-color: rgba(0,0,0,0.12);
}
.switch label input[type=checkbox][disabled]+.lever:after,
.switch label input[type=checkbox][disabled]:checked+.lever:after {
    background-color: #949494;
}

"""
_html_injector.css(css)


class Switch(CheckBox):
    def __init__(self, checked_color=primary, text_pre="", text_post="", **properties):
        dom_node = self._dom_node = _get_dom_node(self)
        dom_node.querySelector(".checkbox").classList.add("switch")

        span = dom_node.querySelector("span")
        span.classList.add("lever")
        span.removeAttribute("style")

        input = dom_node.querySelector("input")
        input.removeAttribute("style")
        input.style.marginTop = 0

        label = dom_node.querySelector("label")
        label.style.padding = "7px 0"

        self._textnode_pre = _document.createTextNode(text_pre)
        self._textnode_post = _document.createTextNode(text_post)
        label.prepend(self._textnode_pre)
        label.append(self._textnode_post)

        self.checked_color = checked_color or primary

    @property
    def checked_color(self):
        return self._checked_color

    @checked_color.setter
    def checked_color(self, value):
        self._checked_color = value
        self._dom_node.style.setProperty("--color", _get_rgb(value))

    @property
    def text_pre(self):
        return self._textnode_pre.textContent

    @text_pre.setter
    def text_pre(self, value):
        self._textnode_pre.textContent = value

    @property
    def text_post(self):
        return self._textnode_post.textContent

    @text_post.setter
    def text_post(self, value):
        self._textnode_post.textContent = value

    text = text_post  # override the CheckBox property
