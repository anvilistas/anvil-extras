# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import wraps

from . import _router
from ._utils import RedirectInfo, RouteInfo, TemplateInfo, _as_frozen_str_iterable

__version__ = "2.2.3"


def _check_types_common(path, priority, condition):
    if not isinstance(priority, int):
        raise TypeError("the template priority must be an int")
    if condition is not None and not callable(condition):
        raise TypeError("the condition must be None or a callable")
    return _as_frozen_str_iterable(path, "path")


def template(path="", priority=0, condition=None):
    path = _check_types_common(path, priority, condition)

    def template_wrapper(cls):
        info = TemplateInfo(cls, path, condition)
        _router.add_info("template", cls, priority, info)

        cls_init = cls.__init__

        def on_show(sender, **e):
            sender.remove_event_handler("show", on_show)
            # wait till the show event so that this template is the open_form before re-navigating
            _router.launch()

        @wraps(cls_init)
        def init_and_route(self, *args, **kws):
            _router._ready = False
            try:
                cls_init(self, *args, **kws)
                handlers = self.get_event_handlers("show")
                self.set_event_handler("show", on_show)
                # make us the first show event handler and re-add existing
                for handler in handlers:
                    self.add_event_handler("show", handler)
            finally:
                _router.ready = True

        cls.__init__ = init_and_route

        return cls

    return template_wrapper


def redirect(path, priority=0, condition=None):
    path = _check_types_common(path, priority, condition)

    def redirect_wrapper(fn):
        info = RedirectInfo(fn, path, condition)
        _router.add_info("redirect", redirect, priority, info)
        return fn

    return redirect_wrapper


def route(url_pattern="", url_keys=[], title=None, full_width_row=False, template=None):
    """
    the route decorator above any form you want to load in the content_panel
    @routing.route(url_pattern=str,url_keys=List[str], title=str)
    """
    if not isinstance(url_pattern, str):
        raise TypeError(f"url_pattern must be type str not {type(url_pattern)}")
    if not (title is None or isinstance(title, str)):
        raise TypeError(f"title must be type str or None not {type(title)}")
    url_keys = _as_frozen_str_iterable(url_keys, "url_keys")
    template = _as_frozen_str_iterable(template, "template", allow_none=True)

    def route_wrapper(cls):
        info = RouteInfo(cls, template, url_pattern, url_keys, title, full_width_row)
        _router.add_route_info(info)
        return cls

    return route_wrapper


def error_form(cls):
    """optional decorator - this is the error form simply use the decorator above your error Form
    @routing.error_form
    """
    cls._route_props = {"title": None, "layout_props": {}}
    _router._error_form = cls
    return cls
