"""
    AnvilAugment
    Copyright 2020 Stu Cork

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Source code published at https://github.com/s-cork/AnvilAugment
"""

from anvil import js as _js, Component as _Component
import anvil as _anvil
from anvil.js.window import jQuery as _S


def add_event(component, event):
    """component: (instantiated) anvil component
    event: str - any jquery event string
    """
    init(component)  # adds the trigger method to the component type
    if not isinstance(event, str):
        raise TypeError('event must be type str and not ' + type(event))
    _add_event(component, event)

    def handler(e):
        event_args = {'event_type': e.type}
        if event.startswith('key'):
            event_args |= {'key': e.key, 'key_code': e.keyCode, 'shift_key': e.shiftKey,
                           'alt_key': e.altKey, 'meta_key': e.metaKey, 'ctrl_key': e.ctrlKey}
        if component.raise_event(event, **event_args):
            e.preventDefault()

    js_event_name = 'mouseenter mouseleave' if event is 'hover' else event
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
        raise TypeError("expected a component not {}".format(
            type(component).__name__))
    if hasattr(component, 'trigger'):
        return
    else:
        component.trigger = trigger


def trigger(self, event):
    """trigger an event on a component, self is an anvil component, event is a component, event is a str or a dictionary
    if event is a dictionary it should include an event key e.g. {'event': 'keypress', 'which': 13}
    """
    if isinstance(event, dict):
        event = _S.Event(event['event'], event)
    event = 'mouseenter mouseleave' if event is 'hover' else event
    _get_jquery_for_component(self).trigger(event)


def _get_jquery_for_component(component):
    if isinstance(component, _anvil.Button):
        return _S(_js.get_dom_node(component).firstElementChild)
    elif isinstance(component, _anvil.FileLoader):
        return _S(_js.get_dom_node(component)).find('form')
    else:
        return _S(_js.get_dom_node(component))


def _add_event(component, event):
    _js.call_js('_add_event', component, event)


# the following is a bit of a hack so that an anvil component knows about its new event names
_ = _js.window.document.createElement('script')
_js.window.document.body.appendChild(_)
_.textContent = 'function _add_event(c, e) { PyDefUtils.unwrapOrRemapToPy(c)._anvil.eventTypes[e] = {name: e} }'


if __name__ == '__main__':
    _ = _anvil.ColumnPanel()
    _.set_event_handler('show', lambda **e: _anvil.Notification(
        'oops AnvilAugment is a dependency', timeout=None).show())
    _anvil.open_form(_)

_ = None
