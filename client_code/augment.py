# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import partial as _partial
from functools import wraps as _wraps

import anvil as _anvil
from anvil import Component as _Component
from anvil import DataGrid as _DataGrid
from anvil import js as _js
from anvil.js.window import WeakMap as _WeakMap
from anvil.js.window import jQuery as _S

from .utils._deprecated import deprecated

__version__ = "3.0.0"

__all__ = ["add_event", "add_event_handler", "set_event_handler", "trigger"]

_Callable = type(lambda: None)
_prefix = "x-augmented-"

# because Skulpt doesn't have a WeakMap and js WeakMap preserves identity of methods
_wm = _WeakMap()


def _weak_cache_event(fn):
    @_wraps(fn)
    def wrapper(instance, event: str):
        event_map = _wm.get(instance)
        if event_map is None:
            _wm.set(instance, {})
            event_map = _wm.get(instance)
        if event not in event_map:
            event_map[event] = fn(instance, event)
        return event_map[event]

    return wrapper


# use cache so we don't add the same event to the component multiple times
# we only need to add the event once and use anvil architecture to raise the event
@_weak_cache_event
def add_event(component: _Component, event: str) -> None:
    """component: (instantiated) anvil component
    event: str - any jquery event string
    """
    if not isinstance(event, str):
        raise TypeError("event must be type str and not " + type(event))

    _add_event(component, event)

    if _has_native_event(component, event):
        return

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


@deprecated(
    "trigger('writeback') is no longer supported\nYou can now trigger a writeback using component.raise_event('x-anvil-write-back-<property>')"
)
def _trigger_writeback(self):
    return


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


def _noop(**e):
    pass


_remap = set()
_native = set()


def _add_event(self, event_name):
    key = (type(self), event_name)
    if key in _native or key in _remap:
        return
    try:
        self.add_event_handler(event_name, _noop)
    except ValueError:
        _remap.add(key)
    else:
        _native.add(key)
        self.remove_event_handler(event_name, _noop)


@_weak_cache_event
def _get_handler(fn, event):
    @_wraps(fn)
    def wrap_handler(*args, **kws):
        kws["event_name"] = event
        return fn(*args, **kws)

    return wrap_handler


def wrap_event_method(method):
    old_method = getattr(_Component, method)

    @_wraps(old_method)
    def wrapped(self, event_name, *args, **kws):
        key = (type(self), event_name)
        if key not in _remap:
            return old_method(self, event_name, *args, **kws)

        remapped = _prefix + event_name

        if len(args) == 1 and callable(args[0]):
            args = [_get_handler(args[0], event_name)]

        return old_method(self, remapped, *args, **kws)

    setattr(_Component, method, wrapped)


for method in [
    "raise_event",
    "add_event_handler",
    "set_event_handler",
    "remove_event_handler",
]:
    wrap_event_method(method)


def _has_native_event(self, event):
    key = (type(self), event)
    return key in _native


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
