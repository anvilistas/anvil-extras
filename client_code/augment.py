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

import anvil as _anvil
from anvil import Component as _Component
from anvil import js as _js
from anvil.js.window import jQuery as _S

__version__ = "1.1.0"


def add_event(component, event):
    """component: (instantiated) anvil component
    event: str - any jquery event string
    """
    init(component)  # adds the trigger method to the component type
    if not isinstance(event, str):
        raise TypeError("event must be type str and not " + type(event))
    _add_event(component, event)

    def handler(e):
        event_args = {"event_type": e.type}
        if event.startswith("key"):
            event_args |= {
                "key": e.key,
                "key_code": e.keyCode,
                "shift_key": e.shiftKey,
                "alt_key": e.altKey,
                "meta_key": e.metaKey,
                "ctrl_key": e.ctrlKey,
            }
        if component.raise_event(event, **event_args):
            e.preventDefault()

    js_event_name = "mouseenter mouseleave" if event == "hover" else event
    _get_jquery_for_component(component).off(js_event_name)
    _get_jquery_for_component(component).on(js_event_name, handler)


def set_event_handler(component, event, func):
    """component: (instantiated) anvil compoent
    event: str - any jquery event string
    func: function to handle the event
    """
    add_event(component, event)
    component.set_event_handler(event, func)


def init(component):
    """adds a trigger method to all components of the type passed"""
    if isinstance(component, _Component):
        component = type(component)
    elif issubclass(component, _Component):
        pass
    else:
        raise TypeError("expected a component not {}".format(type(component).__name__))
    if hasattr(component, "trigger"):
        return
    else:
        component.trigger = trigger


def trigger(self, event):
    """trigger an event on a component, self is an anvil component, event is a component, event is a str or a dictionary
    if event is a dictionary it should include an event key e.g. {'event': 'keypress', 'which': 13}
    """
    if isinstance(event, dict):
        event = _S.Event(event["event"], event)
    event = "mouseenter mouseleave" if event == "hover" else event
    _get_jquery_for_component(self).trigger(event)


def _get_jquery_for_component(component):
    if isinstance(component, _anvil.Button):
        return _S(_js.get_dom_node(component).firstElementChild)
    elif isinstance(component, _anvil.FileLoader):
        return _S(_js.get_dom_node(component)).find("form")
    else:
        return _S(_js.get_dom_node(component))


def _add_event(component, event):
    _js.call_js("_add_event", component, event)


# the following is a bit of a hack so that an anvil component knows about its new event names
_ = _js.window.document.createElement("script")
_js.window.document.body.appendChild(_)
_.textContent = "function _add_event(c, e) { PyDefUtils.unwrapOrRemapToPy(c)._anvil.eventTypes[e] = {name: e} }"


if __name__ == "__main__":
    _ = _anvil.ColumnPanel()
    _.set_event_handler(
        "show",
        lambda **e: _anvil.Notification(
            "oops AnvilAugment is a dependency", timeout=None
        ).show(),
    )
    _anvil.open_form(_)

_ = None
