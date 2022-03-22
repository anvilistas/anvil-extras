# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import wraps
from itertools import chain

from anvil import get_open_form, open_form
from anvil.js.window import document

from ._alert import handle_alert_unload as _handle_alert_unload
from ._logging import logger
from ._utils import get_url_components

__version__ = "2.0.1"


class NavigationExit(Exception):
    pass


class _StackDepthContext:
    def __init__(self):
        self.stack_depth = 0

    def __enter__(self):
        if self.stack_depth <= 5:
            self.stack_depth += 1
            return
        logger.debug(
            "**WARNING**"
            "\nurl_hash redirected too many times without a form load, getting out\ntry setting redirect=False"
        )
        raise NavigationExit

    def __exit__(self, exc_type, *args):
        self.stack_depth -= 1
        if exc_type is NavigationExit:
            return True


def _update_key(key):
    if type(key) is str:
        key = (key, type(get_open_form()).__name__)
    return key


def _wrap_method(method):
    @wraps(method)
    def wrapped(self, key, *args):
        return method(self, _update_key(key), *args)

    return wrapped


class _Cache(dict):
    __getitem__ = _wrap_method(dict.__getitem__)
    __setitem__ = _wrap_method(dict.__setitem__)
    __delitem__ = _wrap_method(dict.__delitem__)
    get = _wrap_method(dict.get)
    pop = _wrap_method(dict.pop)
    setdefault = _wrap_method(dict.setdefault)


stack_depth_context = _StackDepthContext()
default_title = document.title

_current_form = None
_cache = _Cache()
_routes = {}
_templates = set()
_ordered_templates = {}
_error_form = None
_ready = False
_queued = []


def launch():
    global _ready
    _ready = True
    if not _queued:
        return navigate()

    # only run the last _queued navigation
    url_args, properties = _queued.pop()
    _queued.clear()
    navigate(*url_args, **properties)


def navigate(url_hash=None, url_pattern=None, url_dict=None, **properties):
    if not _ready:
        logger.debug(
            f"routing is not ready or the template has not finished loading: queuing the call {url_hash!r}"
        )
        _queued.append([(url_hash, url_pattern, url_dict), properties])
        return
    if url_hash is None:
        url_hash, url_pattern, url_dict = get_url_components()
    logger.debug(
        f"navigation triggered\n\turl_hash    = {url_hash!r}"
        f"\n\turl_pattern = {url_pattern!r}\n\turl_dict    = {url_dict}"
    )
    global _current_form
    with stack_depth_context:
        handle_alert_unload()
        handle_form_unload()
        template_info = load_template(url_pattern)
        url_args = {
            "url_hash": url_hash,
            "url_pattern": url_pattern,
            "url_dict": url_dict,
        }
        alert_on_navigation(**url_args)
        clear_container()
        form = _cache.get(url_hash)
        if form is None:
            form = get_form_to_add(
                template_info, url_hash, url_pattern, url_dict, properties
            )
        else:
            logger.debug(f"{form.__class__.__name__!r} loading from cache")
        _current_form = form
        update_form_attrs(form)
        add_form_to_container(form)
        alert_form_loaded(form=form, **url_args)


def handle_alert_unload():
    if _handle_alert_unload():
        logger.debug("unload prevented by active alert")
        raise NavigationExit


def handle_form_unload():
    before_unload = getattr(_current_form, "before_unload", None)
    if before_unload is None:
        return
    from . import _navigation

    with _navigation.PreventUnloading():
        if before_unload():
            logger.debug(f"stop unload called from {_current_form.__class__.__name__}")
            _navigation.stopUnload()
            raise NavigationExit


def load_template(url_hash):
    global _current_form
    form = get_open_form()
    current_cls = type(form)
    if form is not None and current_cls not in _templates:
        raise NavigationExit  # not using templates

    logger.debug("Checking routing templates")
    for template_info in chain.from_iterable(_ordered_templates.values()):
        cls, path, condition = template_info
        if not url_hash.startswith(path):
            continue
        if condition is None:
            break
        elif condition():
            break
    else:
        load_error_or_raise(f"No template for {url_hash!r}")
    if current_cls is cls:
        logger.debug(f"{cls.__name__!r} routing template unchanged")
        return template_info
    else:
        logger.debug(
            f"{current_cls.__name__!r} routing template changed to {cls.__name__!r}, exiting this navigation call"
        )
        _current_form = None
        f = cls()
        logger.debug(f"form template loaded {cls.__name__!r}, re-navigating")
        open_form(f)
        raise NavigationExit


def alert_on_navigation(**url_args):
    f = get_open_form()
    on_navigation = getattr(f, "on_navigation", None)
    if on_navigation is not None:
        logger.debug(f"{f.__class__.__name__}.on_navigation() called")
        on_navigation(unload_form=_current_form, **url_args)


def clear_container():
    get_open_form().content_panel.clear()


def get_form_to_add(template_info, url_hash, url_pattern, url_dict, properties):
    global _current_form
    route_info, dynamic_vars = path_matcher(
        template_info, url_hash, url_pattern, url_dict
    )

    # check if path is cached with another template
    if len(route_info.templates) > 1:
        for template in route_info.templates:
            form = _cache.get((url_hash, template), None)
            if form is not None:
                logger.debug(
                    f"Loading {form.__class__.__name__!r} from cache - cached with {template!r}"
                )
                return form

    form = route_info.form.__new__(route_info.form, **properties)
    logger.debug(f"adding {form.__class__.__name__!r} to cache")
    _current_form = _cache[url_hash] = form
    form._routing_props = {
        "title": route_info.title,
        "layout_props": {"full_width_row": route_info.fwr},
    }
    form.url_keys = route_info.url_keys
    form.url_pattern = url_pattern
    form.url_dict = url_dict
    form.url_hash = url_hash
    form.dynamic_vars = dynamic_vars
    form.__init__(**properties)  # this might be slow if it does a bunch of server calls
    if _current_form is not form:
        logger.debug(
            f"Problem loading {form.__class__.__name__!r}. Another form was during the call to __init__. exiting this navigation"
        )
        # and if it was slow, and some navigation happened we should end now
        raise NavigationExit
    return form


def load_error_or_raise(msg):
    if _error_form is not None:
        load_error_form()
        raise NavigationExit
    else:
        raise LookupError(msg)


def path_matcher(template_info, url_hash, url_pattern, url_dict):
    given_parts = url_pattern.split("/")
    num_given_parts = len(given_parts)

    valid_routes = _routes.get(template_info.form.__name__, []) + _routes.get(None, [])

    for route_info in valid_routes:
        if not route_info.url_pattern.startswith(template_info.path):
            route_info = route_info._replace(
                url_pattern=template_info.path + route_info.url_pattern
            )
        if num_given_parts != len(route_info.url_parts):
            # url pattern CANNOT fit, skip deformatting
            continue

        dynamic_vars = {}
        for given, (url_part, is_dynamic) in zip(given_parts, route_info.url_parts):
            if is_dynamic:
                dynamic_vars[url_part] = given
            elif url_part != given:
                break
        else:  # no break
            if set(url_dict) == route_info.url_keys:
                return route_info, dynamic_vars

    logger.debug(
        f"no route form with:\n\turl_pattern={url_pattern!r}\n\turl_keys={list(url_dict.keys())}"
        f"\n\ttemplate={template_info.form.__name__!r}\n"
        "If this is unexpected perhaps you haven't imported the form correctly"
    )
    load_error_or_raise(f"{url_hash!r} does not exist")


def update_form_attrs(form):
    url_hash, url_pattern, url_dict = get_url_components()
    # reapply these before the show event
    form.url_hash = url_hash
    form.url_pattern = url_pattern
    form.url_dict = url_dict
    title = getattr(form, "_routing_props", {}).get("title")
    if title is None:
        document.title = default_title
        return
    try:
        document.title = title.format(**url_dict, **getattr(form, "dynamic_vars", {}))
    except Exception:
        raise ValueError(
            "Error generating the page title. Please check the title argument in the decorator."
        )


def add_form_to_container(form):
    if form.parent:
        # I may have been used within another template so remove me from my parent
        form.remove_from_parent()
    layout_props = getattr(form, "_routing_props", {}).get("layout_props", {})
    cp = get_open_form().content_panel
    cp.clear()  # clear it again
    cp.add_component(form, **layout_props)


def alert_form_loaded(**url_args):
    f = get_open_form()
    on_form_load = getattr(f, "on_form_load", None)
    if on_form_load is not None:
        logger.debug(f"{f.__class__.__name__}.on_form_load() called")
        on_form_load(**url_args)


def load_error_form():
    global _error_form, _current_form
    logger.debug(f"loading error form: {_error_form!r}")
    url_hash, _, _ = get_url_components()
    _cache[url_hash] = _error_form()
    _current_form = _cache[url_hash]
    f = get_open_form()
    if f is not None:
        add_form_to_container(_current_form)
    else:
        open_form(_current_form)  # just in case we somehow don't have a valid template!


def add_route_info(route_info):
    logger.debug(
        "   route registered: (form={form.__name__!r}, url_pattern={url_pattern!r}, url_keys={url_keys}, title={title!r})".format(
            **route_info._asdict()
        )
    )
    for template in route_info.templates:
        _routes.setdefault(template, []).append(route_info)


def add_template_info(cls, priority, template_info):
    global _ordered_templates, _templates
    logger.debug(
        "template registered: (form={form.__name__!r}, path={path!r}, priority={priority}, condition={condition})".format(
            priority=priority, **template_info._asdict()
        )
    )
    _templates.add(cls)
    current = _ordered_templates
    current.setdefault(priority, []).append(template_info)
    ordered = {}
    for priority in sorted(current, reverse=True):
        # rely on insertion order
        ordered[priority] = current[priority]
    _ordered_templates = ordered
