# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from anvil import Label, Link, get_open_form, set_url_hash

from .utils._view_transition import ViewTransition, use_transitions

__version__ = "3.1.0"

# A dict mapping a form's name to a further dict with the form's class and title
_forms = {}

# A list of all navigation links
_links = []

# A dict mapping an event name to list of dicts.
# Each of those dicts has keys "link" and "visible" with values of a link instance
# and boolean respectively. The boolean is used to set the 'visible' property of the
# link when the event is raised.
_visibility = {}

_title_label = Label()

_default_mode = "classic"


def _validate_mode(mode):
    if mode not in ("classic", "hash"):
        raise ValueError(
            "A navigation link's routing must either be 'classic' or 'hash'"
        )


def set_mode(mode):
    global _default_mode
    _validate_mode(mode)
    _default_mode = mode


class register:
    """A decorator to register a form as a navigation target (only use in classic mode)"""

    def __init__(self, name, title=None):
        self.name = name
        self.title = title

    def __call__(self, cls):
        _forms[self.name] = {"class": cls, "title": self.title}
        return cls


def get_form(name, *args, **kwargs):
    """Create an instance of a registered form."""
    try:
        return _forms[name]["class"](*args, **kwargs)
    except KeyError:
        raise KeyError(f"No form registered under name: {name}")


def set_title(text):
    _title_label.text = text


def open_form(form_name, *args, full_width=False, **kwargs):
    """Use classic routing to open a registered form"""
    form = get_form(form_name, *args, **kwargs)
    with ViewTransition(form):
        title = _forms[form_name]["title"]
        if title is not None:
            set_title(title)
        get_open_form().content_panel.clear()
        get_open_form().content_panel.add_component(form, full_width_row=full_width)


def go_to(target):
    """Emulate clicking a menu link"""
    for link in _links:
        if link.tag.target == target:
            break
    else:  # no break
        raise ValueError(f"No menu link matching target: {target}")
    link.raise_event("click")


def _reset_links():
    for link in _links:
        if isinstance(link.role, str):
            link.role = [link.role]
        try:
            link.role = [r for r in link.role if r != "selected"]
        except TypeError:
            link.role = []


_actions = {"classic": open_form, "hash": set_url_hash}


def _default_link_click(**event_args):
    """A handler for navigation link click events
    * Clears the role of all links registered in this module
    * Set the calling link's role to 'selected'
    * Calls the relevant action for classic or hash routing
    """
    _reset_links()
    link = event_args["sender"]
    link.role += ["selected"]

    kwargs = {}
    if link.tag.routing == "classic":
        kwargs["full_width"] = link.tag.full_width
    if link.tag.title is not None:
        set_title(link.tag.title)
    _actions[link.tag.routing](link.tag.target, **kwargs)


def _visibility_event_handler(**event_args):
    """A handler for all registered visibility events"""
    items = _visibility[event_args["event_name"]]
    for item in items:
        item["link"].visible = item["visible"]


def _register_visibility(container, link, visibility):
    """Register the visibility events and set the handler on the container"""
    for event, visible in visibility.items():
        if event not in _visibility:
            _visibility[event] = []
            container.set_event_handler(event, _visibility_event_handler)
        _visibility[event].append({"link": link, "visible": bool(visible)})


def build_menu(container, items, with_title=True):
    """Add links to the container and set their initial visibility"""
    _title_label.remove_from_parent()
    if with_title:
        container.parent.add_component(_title_label, slot="title")
    for item in items:
        link = navigation_link(**item)
        _links.append(link)
        visibility = link.tag.visibility
        if visibility is None:
            link.visible = not link.tag.condition
        else:
            link.visible = False
            _register_visibility(container, link, visibility)
        container.add_component(link)
    check_conditions()


def check_conditions():
    for link in _links:
        condition = link.tag.condition
        if condition is None:
            continue
        link.visible = bool(condition())


def navigation_link(
    routing=None,
    full_width=False,
    target=None,
    title=None,
    on_click=None,
    visibility=None,
    condition=None,
    **kwargs,
):
    """Create a link instance

    Parameters
    ----------
    full_width
      Whether the link target should open as full width
    target
      Either the name of a registered form for classic routing or
      a url_hash for hash routing
    title
      sets the page title when this link is clicked
    on_click
      event handler to call when clicked
    visibility
      a dict mapping the names of events to either True or False
    condition
      a callable to determine whether a link is visible or not
    kwargs
      will be passed the Link constructor
    """
    routing = routing or _default_mode
    _validate_mode(routing)

    link = Link(**kwargs)
    link.tag.routing = routing
    link.tag.full_width = full_width
    link.tag.target = target
    link.tag.visibility = visibility
    link.tag.title = title
    link.tag.condition = condition
    if on_click is None:
        link.set_event_handler("click", _default_link_click)
    else:
        link.set_event_handler("click", on_click)
    return link
