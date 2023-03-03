# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import cache as _cache
from functools import partial as _partial

import anvil as _anvil
from anvil import Component as _Component
from anvil import DataGrid as _DataGrid
from anvil import js as _js
from anvil.js.window import Function as _Function
from anvil.js.window import jQuery as _S

__version__ = "2.2.3"

__all__ = ["add_event", "add_event_handler", "set_event_handler", "trigger"]

_Callable = type(lambda: None)


# use cache so we don't add the same event to the component multiple times
# we only need to add the event once and use anvil architecture to raise the event
@_cache
def add_event(component: _Component, event: str) -> None:
    """component: (instantiated) anvil component
    event: str - any jquery event string
    """
    if not isinstance(event, str):
        raise TypeError("event must be type str and not " + type(event))
    _add_event(component, event)

    def handler(e):
        handleObj = e.get("handleObj")
        if handleObj is None:
            type = e.type
        else:
            type = handleObj.get("origType") or e.type
        event_args = {"event_type": type, "original_event": e}
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
    _get_jquery_for_component(component).on(js_event_name, handler)


def set_event_handler(component: _Component, event: str, func: _Callable) -> None:
    """uses anvil's set_event_handler for any jquery event"""
    add_event(component, event)
    component.set_event_handler(event, func)


def add_event_handler(component: _Component, event: str, func: _Callable) -> None:
    """uses anvil's add_event_handler for any jquery event"""
    add_event(component, event)
    component.add_event_handler(event, func)


def remove_event_handler(component: _Component, event: str, func: _Callable) -> None:
    """equivalent to anvil's remove_event_handler"""
    component.remove_event_handler(event, func)


_trigger_writeback = _Function(
    "self",
    """
    self = PyDefUtils.unwrapOrRemapToPy(self);
    const mapPropToWriteback = (p) => () => PyDefUtils.suspensionFromPromise(self._anvil.dataBindingWriteback(self, p.name));
    const customPropsToWriteBack = (self._anvil.customComponentProperties || []).filter(p => p.allow_binding_writeback).map(mapPropToWriteback);
    const builtinPropsToWriteBack = self._anvil.propTypes.filter(p => p.allowBindingWriteback).map(mapPropToWriteback);
    return Sk.misceval.chain(Sk.builtin.none.none$, ...customPropsToWriteBack, ...builtinPropsToWriteBack);
""",
)


def trigger(self: _Component, event: str):
    """trigger an event on a component, self is an anvil component, event is a str or a dictionary
    if event is a dictionary it should include an 'event' key e.g. {'event': 'keypress', 'which': 13}
    """
    if event == "writeback":
        return _trigger_writeback(self)
    if isinstance(event, dict):
        event = _S.Event(event["event"], event)
    event = "mouseenter mouseleave" if event == "hover" else event
    _get_jquery_for_component(self).trigger(event)


_Component.trigger = trigger


def _get_jquery_for_component(component):
    if isinstance(component, _anvil.Button):
        return _S(_js.get_dom_node(component).firstElementChild)
    elif isinstance(component, _anvil.FileLoader):
        return _S(_js.get_dom_node(component)).find("form")
    elif isinstance(component, (_anvil.CheckBox, _anvil.RadioButton)):
        return _S(_js.get_dom_node(component)).find("input")
    else:
        return _S(_js.get_dom_node(component))


_add_event = _Function(
    "self",
    "event",
    """
    self = PyDefUtils.unwrapOrRemapToPy(self);
    self._anvil.eventTypes[event] = self._anvil.eventTypes[event] || {name: event};
""",
)


old_data_grid_event_handler = _DataGrid.set_event_handler


def datagrid_set_event_handler(self, event, handler):
    if event == "pagination_click":
        _set_pagination_handlers(self, handler)
    else:
        old_data_grid_event_handler(self, event, handler)


_DataGrid.set_event_handler = datagrid_set_event_handler


def _prevent_disabled(js_event):
    if js_event.currentTarget.classList.contains("disabled"):
        js_event.stopPropagation()


def _wrap_js_event(handler):
    def wrapper(e):
        handler()

    return wrapper


def _set_pagination_handlers(data_grid, handler):
    grid_dom = _js.get_dom_node(data_grid)
    for name in ["first", "last", "previous", "next"]:
        btn = grid_dom.querySelector(f".{name}-page")
        # use True so that we capture this event before the anvil click event
        btn.addEventListener("click", _prevent_disabled, True)
        btn.addEventListener(
            "click",
            _wrap_js_event(
                _partial(
                    handler,
                    sender=data_grid,
                    button=name,
                    event_name="pagination_click",
                )
            ),
        )
        # note we don't tidy this up - we should probably call removeEventListener
        # but this will be called from code and is unlikely that the user will call this function twice


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
